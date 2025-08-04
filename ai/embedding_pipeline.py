# File: ai/embedding_pipeline.py

import pandas as pd
import numpy as np
import openai
import faiss
import snowflake.connector
from tqdm import tqdm
import os
from dotenv import load_dotenv

# STEP 0: Load environment variables
load_dotenv(dotenv_path='creds.env')

# STEP 1: Set credentials from .env
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_WAREHOUSE = 'demo_wh'
SNOWFLAKE_DATABASE = 'customer_insights'
SNOWFLAKE_SCHEMA = 'raw_data'
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

# STEP 2: Connect to Snowflake and extract support + feedback
print("🔗 Connecting to Snowflake...")
conn = snowflake.connector.connect(
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    account=SNOWFLAKE_ACCOUNT,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)

query = """
SELECT 
  feedback_id AS "id", 
  customer_id AS "customer_id", 
  comment AS "text"
FROM feedback

UNION ALL

SELECT 
  ticket_id AS "id", 
  customer_id AS "customer_id", 
  text AS "text"
FROM support_tickets;
"""

print("📥 Fetching data from Snowflake...")
df = pd.read_sql(query, conn)
print(f"✅ Retrieved {len(df)} rows")

# STEP 3: Generate OpenAI embeddings
def get_embedding(text, model="text-embedding-3-small"):
    try:
        response = openai.Embedding.create(
            model=model,
            input=text
        )
        return response['data'][0]['embedding']
    except Exception as e:
        print(f"⚠️ Error embedding: {text[:30]}... | {e}")
        return None

print("🔄 Generating embeddings with OpenAI...")
tqdm.pandas()
df["embedding"] = df["text"].progress_apply(lambda x: get_embedding(str(x)))

# STEP 4: Filter and save
df.dropna(subset=["embedding"], inplace=True)
print(f"✅ {len(df)} rows successfully embedded.")

# STEP 5: Store in FAISS index
dimension = len(df["embedding"].iloc[0])
index = faiss.IndexFlatL2(dimension)
vectors = np.array(df["embedding"].tolist()).astype("float32")
index.add(vectors)

# Save FAISS index + metadata
print("💾 Saving FAISS index and metadata...")
faiss.write_index(index, "support_feedback_index.faiss")
df[["id", "customer_id", "text"]].to_parquet("feedback_ticket_metadata.parquet", index=False)

print("🎉 Embedding pipeline complete!")
