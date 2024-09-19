# MANTISBT AI Automation

## Descrição do Projeto

Este projeto consiste em uma aplicação que utiliza Inteligência Artificial (IA) para analisar, resumir e propor soluções automatizadas para chamados de TI capturados pela plataforma **MANTISBT**. A IA integra-se ao MANTISBT para fornecer insights automáticos, sugerindo soluções potenciais com base em análise de dados e aprendizado de máquina.

Além disso, o projeto utiliza **Terraform** para provisionar a infraestrutura na **AWS**, incluindo repositórios de imagens Docker no **ECR**, execução de containers no **ECS Fargate**, **RDS** para persistência de dados, e um balanceador de carga com suporte a HTTPS.

## Estrutura do Projeto

A estrutura do repositório está organizada da seguinte forma:

```bash
.
├── app          # Código-fonte da aplicação Django
├── deploy       # Scripts e configuração para deploy da aplicação
├── nginx        # Configuração do servidor Nginx para balanceamento de carga
└── terraform    # Definições de infraestrutura como código usando Terraform
```

## AWS Infrastructure

### Networking
- **VPC**: Virtual Private Cloud para isolar a infraestrutura da aplicação.
- **Public and Private Subnets**: Sub-redes públicas e privadas para distribuir os recursos de forma segura e escalável.
- **Routing Tables**: Tabelas de roteamento para gerenciar o tráfego de rede entre as sub-redes.
- **Internet Gateway**: Permite a comunicação de saída para a internet a partir das sub-redes públicas.

### Security Groups
- Grupos de segurança configurados para controlar o tráfego de entrada e saída para os recursos da AWS, como ECS e RDS.

### Load Balancers, Listeners, and Target Groups
- **Load Balancer**: Distribuidor de tráfego para balancear a carga entre múltiplas instâncias de containers.
- **Listeners**: Responsáveis por escutar as requisições no Load Balancer e direcioná-las para os Target Groups.
- **Target Groups**: Conjunto de containers que receberão o tráfego balanceado.

### IAM Roles and Policies
- **IAM Roles**: Perfis de permissões atribuídos aos recursos, permitindo que ECS e outros serviços da AWS interajam de forma segura.
- **IAM Policies**: Políticas que definem permissões detalhadas para os serviços e recursos AWS.

### ECS
- **Task Definition**: Definição de tarefa com múltiplos containers, incluindo a configuração de rede, recursos (CPU, memória), e volumes.
- **Cluster**: Conjunto de instâncias do ECS onde as tarefas são executadas.
- **Service**: Garante que a quantidade desejada de tarefas esteja sempre em execução no cluster.

### Auto Scaling Config
- Configuração de auto scaling para ajustar dinamicamente o número de containers com base na demanda de tráfego ou uso de recursos.

### RDS
- Banco de dados relacional configurado para persistência de dados, utilizando o serviço **Amazon RDS** com alta disponibilidade e backups automáticos.

### Health Checks and Logs
- **Health Checks**: Verificações automáticas de integridade para monitorar o estado dos containers e recursos.
- **Logs**: Armazenamento de logs de aplicação e de sistema utilizando serviços como **CloudWatch** para monitoramento e análise.


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