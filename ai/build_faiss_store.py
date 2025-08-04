# ai/build_faiss_store.py

from dotenv import load_dotenv
import os
import pandas as pd
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.docstore.document import Document

load_dotenv(dotenv_path='creds.env')
embedding = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Load text + metadata
metadata_df = pd.read_parquet("feedback_ticket_metadata.parquet")

docs = [
    Document(
        page_content=row["text"],
        metadata={"id": row["id"], "customer_id": row["customer_id"]}
    )
    for _, row in metadata_df.iterrows()
]

# ✅ Create and save FAISS store
db = FAISS.from_documents(docs, embedding)
db.save_local("faiss_store")

print("✅ FAISS vector store built and saved locally.")
