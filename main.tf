# Provider Configuration
terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"  # Or latest stable version
    }
  }
}

provider "aws" {
  region = "your-aws-region" # Substitua pela sua região da AWS
}

# ECR Repository for Images
resource "aws_ecr_repository" "web_image_repo" {
  name                 = "api_mantis_web"
  image_tag_mutability = "MUTABLE"
}

resource "aws_ecr_repository" "nginx_image_repo" {
  name                 = "api_mantis_nginx"
  image_tag_mutability = "MUTABLE"
}

# ECS Cluster
resource "aws_ecs_cluster" "api_mantis_cluster" {
  name = "api_mantis_cluster"
}

# Task Definitions (One for Web, One for Nginx)
resource "aws_ecs_task_definition" "web" {
  family                   = "api_mantis_web_task"
  container_definitions    = <<DEFINITION
[
  {
    "name": "api_mantis_web",
    "image": "${aws_ecr_repository.web_image_repo.repository_url}:latest", 
    "portMappings": [
      {
        "containerPort": 8000,
        "hostPort": 8000
      }
    ],
    "environment": [
      # Adicione suas variáveis de ambiente aqui
    ]
  }
]
DEFINITION
  requires_compatibilities = ["FARGATE"]
  cpu                      = 256
  memory                   = 512
  network_mode             = "awsvpc"
  execution_role_arn       = aws_iam_role.ecs_task_execution_role.arn
}

resource "aws_ecs_task_definition" "nginx" {
  # ... (Similar structure to the 'web' task definition, using the Nginx image)
}

# ECS Service (Manages Tasks)
resource "aws_ecs_service" "api_mantis_service" {
  name            = "api_mantis_service"
  cluster         = aws_ecs_cluster.api_mantis_cluster.id
  task_definition = aws_ecs_task_definition.web.arn
  desired_count   = 1 
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = [aws_subnet.public.*.id]
    security_groups  = [aws_security_group.ecs_tasks.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api_mantis_target_group.arn
    container_name   = "api_mantis_web"
    container_port   = 8000
  }

  depends_on = [aws_lb.api_mantis_lb]
}

# ... (Rest of the configuration: ALB, Security Groups, VPC, etc.)
