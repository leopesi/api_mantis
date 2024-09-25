# MantisBT AI Automation

## Descrição 

Este projeto integra IA para analisar, resumir e propor soluções automatizadas para chamados de TI no MantisBT, utilizando GitLab CI para pipeline de build/deploy. A infraestrutura é provisionada com Terraform na AWS, com ECR, ECS Fargate, RDS e balanceamento de carga HTTPS.

## Estrutura do Projeto

A estrutura do repositório está organizada da seguinte forma:

```bash
.
├.gitlab-ci.yml  # Pipeline Build e Deploy
├── app          # Código-fonte da aplicação Django
├── deploy       # Scripts e configuração para deploy da aplicação
├── nginx        # Configuração do servidor Nginx para balanceamento de carga
└── terraform    # Definições de infraestrutura como código usando Terraform
```

## Arquitetura AWS da Aplicação

Esta arquitetura foi projetada para garantir alta disponibilidade, escalabilidade e segurança.

Componentes principais:

- **VPC**: Duas zonas de disponibilidade.
- **Subnets**: Públicas para acesso à internet e privadas para recursos internos.
- **Load Balancer**: Distribui o tráfego entre as instâncias para alta disponibilidade.
- **EC2**: Instâncias com auto escalamento.
- **ECS**: Maior flexibilidade e escalabilidade.
- **RDS**: PostgreSQL.
- **Routing Tables**: Gerencia o tráfego de rede entre as sub-redes.
- **Auto Scaling**: Ajusta dinamicamente o número de containers com base na demanda de tráfego ou uso de recursos.
- **Internet Gateway**: Permite a comunicação de saída para a internet a partir das sub-redes públicas.
  
Fluxo:

- O tráfego de internet entra no sistema através do ALB, que está nas sub-redes públicas.
- O ALB distribui esse tráfego para as instâncias ECS rodando nas sub-redes privadas em ambas as zonas de disponibilidade (para alta disponibilidade e balanceamento).
- As instâncias ECS podem se comunicar com o banco de dados RDS PostgreSQL, que está nas sub-redes privadas.
- Para se conectar à internet para atualizações ou outros propósitos, as instâncias nas sub-redes privadas passam pelo NAT Gateway, que está em uma sub-rede pública.
  
Benefícios:

Essa arquitetura garante alta disponibilidade, escalabilidade e segurança, ao isolar serviços sensíveis como o banco de dados em sub-redes privadas e distribuir o tráfego em várias zonas de disponibilidade.

## Tecnologias Utilizadas

- **Python / Django**
- **Inteligência Artificial**
- **MantisBT**
- **Docker**
- **Nginx**
- **GitLab**
- **Terraform**
- **AWS ECS (Fargate)**
- **AWS ECR**
- **AWS RDS**
- **AWS Load Balancer**


## Contribuição

Sinta-se à vontade para abrir issues ou pull requests caso deseje contribuir com o projeto.

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.