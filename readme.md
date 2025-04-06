# Projeto de Automação de Dados com Apache Airflow

Este projeto foi desenvolvido como parte do curso de **Apache Airflow** da **Alura**, com o objetivo de aplicar conceitos de orquestração de dados, automação de tarefas e criação de pipelines ETL utilizando o Airflow.

## Finalidade do Projeto

A proposta central do projeto é:

- **Automatizar a coleta de dados meteorológicos** de uma API externa.
- **Executar essa coleta de forma recorrente (semanalmente ou diariamente)**, usando DAGs do Airflow.
- **Realizar um pequeno processo de ETL**, onde os dados são extraídos da API, organizados em estruturas tabulares e salvos como arquivos CSV.
- Demonstrar o uso de operadores básicos do Airflow: `EmptyOperator`, `BashOperator` e `PythonOperator`.

Essa automação é ideal para casos em que é necessário coletar dados de maneira constante e sistemática, como para alimentar dashboards, relatórios ou análises.

---

## Ferramentas e Tecnologias

- **[Apache Airflow](https://airflow.apache.org/)** – Orquestração dos fluxos de trabalho.
- **Python 3.9** – Linguagem base do projeto.
- **`pandas`** – Manipulação e salvamento de dados tabulares.
- **`python-dotenv`** – Carregamento de variáveis de ambiente (.env).
- **Sistema Operacional**: Ubuntu

---

## Estrutura dos DAGs

A pasta `dags/` contém os DAGs desenvolvidos:

### 🔹 `first_dag.py`

Um DAG simples criado com fins didáticos, contendo:

- **3 tarefas fictícias (EmptyOperator)** para ilustrar dependências e execução paralela/sequencial.
- **1 tarefa com BashOperator** que cria um diretório com timestamp baseado no `data_interval_end`.

**Fluxo da DAG:**
```text
task_1
  ├──> task_2
  └──> task_3 ──> make_dir (criação de diretório local com data)
```

Esse DAG exemplifica a estrutura e execução de tarefas no Airflow, sem lógica de negócio envolvida.

---

### 🔹 `weather_data.py`

Este é o DAG principal e funcional do projeto.

**Objetivo:** automatizar a coleta de dados meteorológicos da API [Open-Meteo](https://open-meteo.com/), salvando os dados de clima em um CSV.

#### Componentes da DAG:

- `extract_weather_data()`:  
  Função Python que consome a API, coleta dados de temperatura diária mínima e máxima, e estrutura os dados em um DataFrame com `pandas`.

- `save_to_csv()`:  
  Função que recebe os dados da tarefa anterior, converte em CSV e salva em disco no diretório `data/`.

#### Lógica do Fluxo:

```text
start (EmptyOperator)
   ↓
extract_weather_data (PythonOperator)
   ↓
save_to_csv (PythonOperator)
   ↓
end (EmptyOperator)
```

O DAG roda semanalmente (`@weekly`) e salva arquivos CSV com a previsão da semana, automatizando completamente a coleta e persistência local.

---

## Uso de Variáveis de Ambiente

A DAG `weather_data.py` utiliza variáveis de ambiente (por exemplo, `API_KEY`) para proteger dados sensíveis. Essas variáveis são carregadas via `.env` e lidas no script com a biblioteca `python-dotenv`.

```python
load_dotenv()
api_key = os.getenv("API_KEY")
```

> O arquivo `.env` **não está versionado** por motivos de segurança.

---

## O que foi aprendido no projeto

- Conceitos de DAGs, operadores e dependências no Apache Airflow.
- Como estruturar pipelines ETL com Python e Airflow.
- Leitura de variáveis externas com `.env`.
- Modularização de tarefas com `PythonOperator` e `BashOperator`.
- Persistência de dados em arquivos CSV.
- Orquestração de tarefas em ambientes de produção de dados.

---

**Desenvolvido como parte do curso [Apache Airflow da Alura](https://cursos.alura.com.br/course/apache-airflow-primeiro-pipeline-dados).**
