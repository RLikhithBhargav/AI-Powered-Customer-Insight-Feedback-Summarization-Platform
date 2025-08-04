# FROM apache/airflow:2.7.2-python3.10

# USER airflow

# RUN pip install --no-cache-dir dbt-core dbt-postgres

FROM apache/airflow:2.7.2-python3.10

USER airflow

# Install all required packages including dbt-snowflake
RUN pip install --no-cache-dir \
    dbt-snowflake \
    openai \
    tqdm \
    pandas \
    python-dotenv \
    snowflake-connector-python

# USER airflow

