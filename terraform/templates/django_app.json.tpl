[
  {
    "name": "django-app",
    "image": "${docker_image_url_django}",
    "essential": true,
    "cpu": 10,
    "memory": 512,
    "portMappings": [
      {
        "containerPort": 8000,
        "protocol": "tcp"
      }
    ],
    "command": ["gunicorn", "-w", "3", "-b", ":8000", "hello_django.wsgi:application"],
    "environment": [
  {
    "name": "RDS_DB_NAME",
    "value": "${rds_db_name}"
  },
  {
    "name": "RDS_USERNAME",
    "value": "${rds_username}"
  },
  {
    "name": "RDS_PASSWORD",
    "value": "${rds_password}"
  },
  {
    "name": "RDS_HOSTNAME",
    "value": "${rds_hostname}"
  },
  {
    "name": "RDS_PORT",
    "value": "5432"
  }
],
    "logConfiguration": {
      "logDriver": "awslogs",
      "options": {
        "awslogs-group": "/ecs/django-app",
        "awslogs-region": "${region}",
        "awslogs-stream-prefix": "django-app-log-stream"
      }
    }
  }
  
]

