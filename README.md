# MANTISBT AI Automation

## Descrição do Projeto

Este projeto consiste em uma aplicação que utiliza Inteligência Artificial (IA) para analisar, resumir e propor soluções automatizadas para chamados de TI capturados pela plataforma **MANTISBT**. A IA integra-se ao MANTISBT para fornecer insights automáticos, sugerindo soluções potenciais com base em análise de dados e aprendizado de máquina.

Além disso, o projeto utiliza **Terraform** para provisionar a infraestrutura na **AWS**, incluindo repositórios de imagens Docker no **ECR**, execução de containers no **ECS Fargate**, **RDS** para persistência de dados, e um balanceador de carga com suporte a HTTPS.

## Estrutura do Projeto

A estrutura do repositório está organizada da seguinte forma:
.
├── app          # Código-fonte da aplicação Django
├── deploy       # Scripts e configuração para deploy da aplicação
├── nginx        # Configuração do servidor Nginx para balanceamento de carga
└── terraform    # Definições de infraestrutura como código usando Terraform



## Tecnologias Utilizadas

- **Python / Django**: Framework web utilizado para desenvolver a aplicação.
- **Inteligência Artificial**: IA implementada para análise e sugestão de soluções para chamados de TI.
- **MANTISBT**: Plataforma de gerenciamento de chamados integrada ao projeto.
- **Docker**: Utilizado para containerizar a aplicação.
- **Nginx**: Servidor web usado para servir a aplicação e gerenciar o balanceamento de carga.
- **Terraform**: Ferramenta para provisionamento de infraestrutura.
- **AWS ECS (Fargate)**: Serviço para orquestração de containers.
- **AWS ECR**: Registro de imagens Docker.
- **AWS RDS**: Banco de dados relacional.
- **AWS Load Balancer**: Utilizado para gerenciar o tráfego com suporte a HTTPS.
- **Boto3**: Biblioteca Python para interagir com serviços AWS.

## Contribuição

Sinta-se à vontade para abrir issues ou pull requests caso deseje contribuir com o projeto.

## Licença

Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para mais detalhes.
