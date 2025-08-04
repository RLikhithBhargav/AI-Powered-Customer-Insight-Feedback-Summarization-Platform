import os
import pandas as pd
from dotenv import load_dotenv
import snowflake.connector
import subprocess
import openai
from tqdm import tqdm

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), 'creds.env')
load_dotenv(dotenv_path)

# Environment variables
SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

RAW_DATA_PATH = "/mnt/raw_data"
AI_PATH = "/mnt/ai"
DBT_PROJECT_PATH = "/mnt/dbt"

def upload_to_snowflake():
    print("Uploading customers.csv to Snowflake...")
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema="RAW_DATA"
    )
    cursor = conn.cursor()
    try:
        cursor.execute("CREATE SCHEMA IF NOT EXISTS RAW_DATA")
        cursor.execute("DROP TABLE IF EXISTS RAW_DATA.CUSTOMERS")
        cursor.execute("""
            CREATE TABLE CUSTOMERS (
                CUSTOMER_ID STRING,
                NAME STRING,
                SIGNUP_DATE DATE,
                AGE INT,
                LOCATION STRING,
                STATUS STRING
            )
        """)
        df = pd.read_csv(f"{RAW_DATA_PATH}/customers.csv")
        for _, row in df.iterrows():
            cursor.execute(
                "INSERT INTO CUSTOMERS VALUES (%s, %s, %s, %s, %s, %s)",
                tuple(row)
            )
        print(f"Uploaded {len(df)} rows to RAW_DATA.CUSTOMERS")
    finally:
        cursor.close()
        conn.close()

def run_dbt_transforms():
    print("Running DBT transforms...")
    try:
        subprocess.run(["dbt", "run", "--project-dir", DBT_PROJECT_PATH], check=True)
        print("DBT completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"DBT run failed with error:\n{e}")
        raise

def export_customer_features():
    print("Exporting FCT_CUSTOMER_FEATURES from Snowflake...")
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema="ANALYTICS"
    )
    cursor = conn.cursor()
    try:
        query = "SELECT * FROM FCT_CUSTOMER_FEATURES"
        cursor.execute(query)
        df = cursor.fetch_pandas_all()
        output_path = f"{AI_PATH}/customer_features.csv"
        df.to_csv(output_path, index=False)
        print(f"Exported {len(df)} rows to: {output_path}")
    finally:
        cursor.close()
        conn.close()

def summarize_text(text, client):
    prompt = f"Summarize this customer feedback in one short sentence: '{text}'"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {e}"

def generate_gpt_summaries():
    print("Generating GPT summaries...")
    openai.api_key = os.getenv("OPENAI_API_KEY")
    input_path = f"{RAW_DATA_PATH}/feedback.csv"
    output_path = f"{AI_PATH}/feedback_with_summary.csv"
    df = pd.read_csv(input_path)
    tqdm.pandas(desc="Summarizing feedback")
    df["summary"] = df["comment"].progress_apply(lambda x: summarize_text(str(x), openai))
    df.to_csv(output_path, index=False)
    print(f"Summaries saved to {output_path}")

def notify_dashboard_ready():
    print("Dashboard data is ready. Launch Streamlit UI manually to view updates.")
