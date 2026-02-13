# 📦 Cálculo de métricas de SLA utilizando a arquitetura Medallion

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
    │   ├── orchestration/
    │   │    └── pipeline.py        # Orquestrador principal
    │   ├── bronze/ 
    │   │    └── ingest_bronze.py
    │   ├── silver/ 
    │   │    └── transform_silver.py
    │   └── gold/
    │       └── build_gold.py
    │
    ├── config/
    │   ├── config_loader.py
    │   ├── settings.py
    │   └── pipeline.yaml         # definição de paths
    │
    ├── data/
    │   ├── bronze/ 
    │   ├── silver/ 
    │   └── gold/
    │
    ├── analytics/
    │   ├── eda.py                 # Análise exploratória
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

## ⏱ 8. Explicação da Lógica de Cálculo do SLA

O cálculo do SLA foi realizado considerando como **dias úteis** todos os
dias que não sejam finais de semana ou feriados.

Para fins de apuração, cada dia útil é tratado como contendo **24 horas
úteis**, ou seja, não há restrição de janela de horário (por exemplo,
08h às 18h). Isso significa que qualquer horário dentro de um dia
classificado como útil é contabilizado no cálculo.

### Regras aplicadas

-   São considerados dias não úteis:
    -   Sábados
    -   Domingos
    -   Feriados oficiais
-   Não há limitação de horário comercial.
-   Se uma issue for resolvida em horários não convencionais (ex:
    madrugada), as horas serão contabilizadas normalmente, desde que o
    dia seja útil.
-   Caso uma issue seja criada e resolvida integralmente em um fim de
    semana ou feriado, o total de horas úteis computadas será **0
    horas**.

### Identificação de Feriados

Para a identificação de feriados, é utilizado o pacote `holidays`,
listado no arquivo `requirements.txt`.

Esse pacote permite determinar programaticamente se uma determinada data
corresponde a um feriado oficial, garantindo consistência no cálculo das
horas úteis.

## 📚 9. Dicionário de Dados

### 9.1 Issues (Tabela final)

Este dataset representa **issues (chamados) do Jira**, contendo
informações sobre responsabilidade, prazos e cumprimento de SLA (Service
Level Agreement).

Cada registro corresponde a um chamado individual.

------------------------------------------------------------------------

### 🔎 Identificação da Issue

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `issue_id` | string | Identificador único da issue no Jira. |
| `issue_type` | string | Tipo da issue (ex: Bug, Task). |
| `status` | string | Status atual ou final da issue (ex: Open, Resolved, Done). |
| `priority` | string | Nível de prioridade definido no Jira (ex: Low, Medium, High). |
| `project_id` | string | Identificador do projeto ao qual a issue pertence. |

---

### 👤 Responsável

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `assignee_id` | string | Identificador único do responsável pela issue. |
| `assignee_name` | string | Nome do responsável pela execução da issue. |
| `assignee_email` | string | Email do responsável. |

---

### 🗓 Datas da Issue

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `created_at` | datetime | Data/hora normalizada de criação da issue. |
| `resolved_at` | datetime | Data/hora normalizada de resolução da issue. |
| `raw_created_at` | string | Data/hora original conforme extraída do Jira (antes de tratamento). |
| `raw_resolved_at` | string | Data/hora original de resolução conforme extraída do Jira (antes de tratamento). |

---

### 🔍 Qualidade de Dados

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `is_created_at_valid` | boolean | Indica se `created_at` passou nas validações de consistência. |
| `is_resolved_at_valid` | boolean | Indica se `resolved_at` passou nas validações de consistência. |
| `dates_quality` | string | Indicador consolidado da qualidade das datas (i.e., VALID, INVALID_CREATED_AND_RESOLVED, INVALID_CREATED_AT, INVALID_RESOLVED_AT). |

---

### ⏱ Métricas de SLA

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `business_hours_to_sla_resolution` | float | Tempo real gasto para resolver a issue, calculado em horas úteis entre `created_at` e `resolved_at`. |
| `expected_sla_hours_to_resolution` | float | Tempo máximo permitido para resolução da issue conforme regra de SLA definida (em horas úteis). |
| `is_sla_violated` | boolean | Indica se o SLA foi violado (True) ou atendido (False). Uma violação ocorre quando o tempo real excede o esperado. |

---

### 9.2 Project

Este dataset representa **Projetos do Jira**, contendo
informações sobre os projetos em que as issues foram abertas.

Cada registro corresponde a um projeto.

| Coluna | Tipo Esperado | Descrição |
| :--- | :--- | :--- |
| `project_id` | string | Identificador do projeto ao qual a issue pertence. |
| `project_name` | string | Nome completo ou descritivo do projeto. |
| `extracted_at` | datetime | Data/hora normalizada em que os dados foram extraídos do sistema. |
| `raw_extracted_at` | string | Data/hora em que os dados foram extraídos do sistema (antes de tratamento). |

### 9.3 Relatórios 

### 📊 SLA Médio por Analista

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `assignee_name` | string | Nome do responsável pela execução da issue. |
| `assignee_id` | string | Identificador único do responsável pela issue. |
| `project_id` | string | Identificador do projeto ao qual a issue pertence. |
| `avg_business_hours_to_sla_resolution` | float | Média de horas úteis gastas para a resolução das issues (valor numérico decimal). |
| `issue_count` | integer | Quantidade total de issues atribuídas ao responsável. |
| `avg_business_hours_to_sla_resolution_hms` | string | Média de tempo de resolução formatada em Horas, Minutos e Segundos (e.g.,: `34:59:56 (34h 59m 56s)`). |

### 📊 SLA Médio por Tipo de Chamado

| Coluna | Tipo | Descrição |
| :--- | :--- | :--- |
| `issue_type` | string | Tipo da issue (ex: Bug, Task). |
| `project_id` | string | Identificador do projeto ao qual a issue pertence. |
| `avg_business_hours_to_sla_resolution` | float | Média de horas úteis gastas para a resolução das issues (valor numérico decimal). |
| `issue_count` | integer | Quantidade total de issues atribuídas ao responsável. |
| `avg_business_hours_to_sla_resolution_hms` | string | Média de tempo de resolução formatada em Horas, Minutos e Segundos (e.g.,: `34:59:56 (34h 59m 56s)`). |
