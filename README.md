# Deploy app Django com Infra AWS: Docker, Terraform e GitLab: Do VPC ao Load Balancer.

## Descrição 

## Integração de Gestão de Incidentes e Automação de Infraestrutura
Esta aplicação une dois mundos: gestão e análise de incidentes de TI com a automação da infraestrutura. De um lado, temos uma aplicação que integra SharePoint com MantisBT e a IA da Gemini, permitindo que os usuários acompanhem e analisem seus tickets de suporte com a IA fazendo uma análise do incidente de acordo com o perfil do usuário. Do outro, uma infraestrutura robusta e automaticamente provisionada na AWS com Terraform e GitLab. Juntas, essas soluções oferecem uma plataforma completa que otimiza tanto o gerenciamento de problemas quanto a entrega de recursos de TI.

## Gestão de Incidentes com SharePoint via Microsoft Graph API e MantisBT
Ferramenta de gestão de incidentes de suporte de TI com Python. Integrada à intranet (Sharepoint) via iframe, utiliza a Microsoft Graph API para captar a Microsoft account do usuário e faz uma requisição na API do MantisBT para captar os tickets associados ao usuário e retorna uma lista com o título e o número do ticket.

O usuário pode pedir uma análise do ticket e então uma outra requisição é enviada para a Gemini API com um script e o json do ticket, que retorna uma análise e resume cada ação aplicada no caso (Se for Global Reader retorna um ambiente de suporte com análise e sugestões de solução do incidente com uma integracação com a IA da Gemini API).

## Deploy Automatizado de Infraestrutura AWS com Terraform e GitLab: Do VPC ao Load Balancer
Infraestrutura (IaC) escrita com Terraform, integrada com GitLab (build/deploy) e versionada com git. Cria uma VPC que define a rede onde os recursos serão implementados. Em seguida, são configuradas as sub-redes públicas e privadas, seguidas pelo grupo de sub-redes do banco de dados.

Depois disso, são configurados os grupos de segurança para controlar o tráfego, incluindo o grupo de segurança do RDS, o do ECS e o do Load Balancer.

Com a rede e a segurança preparadas, a instância do banco de dados RDS é criada, juntamente com o EFS e access point.

Em seguida, a Role IAM necessário para a execução das tarefas ECS é configurado, seguido pela criação do cluster ECS e da Task Definition da aplicação. O Auto Scaling Target para o ECS é então configurado, permitindo a escalabilidade do ECS.

Finalmente, o grupo de destino para o ALB é criado e, por último, é processado o template. Essa sequência garante que todos os recursos necessários estejam prontos antes da criação dos serviços de aplicação e balanceamento de carga.


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
