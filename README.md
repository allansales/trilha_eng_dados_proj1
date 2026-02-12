# 📦 Nome do Projeto

> **Descrição curta:** Pipeline de processamento de dados em Python com
> orquestração modular, integração com Azure e suporte a análise
> exploratória (EDA).

------------------------------------------------------------------------

## 📖 1. Visão Geral

Este projeto implementa um pipeline de dados estruturado, com separação
clara de responsabilidades, uso de variáveis de ambiente para
credenciais e execução modular via `python -m`.

O objetivo é garantir:

-   🔒 Segurança no uso de credenciais
-   🧱 Arquitetura organizada e escalável
-   🔁 Reprodutibilidade do ambiente
-   📊 Suporte a análise exploratória de dados
-   🚀 Facilidade de execução e manutenção

------------------------------------------------------------------------

## 🏗 2. Arquitetura

    .
    ├── src/
    │   └── orchestration/
    │   │    └── pipeline.py        # Orquestrador principal
    │   └── bronze/ 
    │   │    └── ingest_bronze.py
    │   └── silver/ 
    │   │    └── transform_silver.py
    │   └── gold/
    │       └── build_gold.py
    │
    ├── config/
    │   └── config_loader.py
    │   └── settings.py
    │   └── pipeline.yaml         # definição de paths
    │
    ├── data/
    │   └── bronze/ 
    │   └── silver/ 
    │   └── gold/
    │
    ├── analytics/
    │   └── eda.py                 # Análise exploratória
    │   └── report/
    │
    ├── .gitignore
    ├── requirements.txt
    ├── .env.example
    └── README.md

------------------------------------------------------------------------

## 🧰 3. Stack Tecnológica

-   Python 3.10+
-   Azure SDK
-   Virtualenv
-   python-dotenv
-   Outras dependências descritas em `requirements.txt`

------------------------------------------------------------------------

## 📌 4. Pré-requisitos

Antes de iniciar, garanta que você possui:

-   Python 3.10 ou superior
-   pip atualizado
-   Git instalado
-   Acesso às credenciais Azure necessárias

------------------------------------------------------------------------

## ⚙️ 5. Configuração do Ambiente

### 5.1 Clonar o repositório

``` bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_PROJETO>
```

### 5.2 Criar ambiente virtual

#### Windows

``` bash
python -m venv venv
venv\Scripts\activate
```

#### Linux / Mac

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 5.3 Instalar dependências

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🔐 6. Gestão de Variáveis de Ambiente

O projeto utiliza variáveis de ambiente para autenticação e configuração
de serviços.

### 6.1 Criar arquivo `.env`

``` bash
cp .env.example .env
```

> Windows (PowerShell):

``` powershell
copy .env.example .env
```

### 6.2 Configurar credenciais Azure

Edite o arquivo `.env`:

``` env
AZURE_TENANT_ID = <sua_azure_tenant_id>
AZURE_CLIENT_ID = <sua_azure_client_id>
AZURE_CLIENT_SECRET = <sua_azure_client_secret>
```

------------------------------------------------------------------------

## 🚀 7. Execução

Para executar o pipeline ou a análise, os comandos devem ser executados **na raiz do projeto**. A execução do pipeline gerará os dados que serão consumidos pelo EDA.

### 7.1 Pipeline

``` bash
python -m src.orchestration.pipeline
```

### 7.2 Análise Exploratória (EDA)

``` bash
python -m analytics.eda
```