# File: ai/query_agent.py

import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# Load credentials
load_dotenv(dotenv_path='creds.env')
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

# ✅ Load FAISS store the safe way
db = FAISS.load_local("ai/faiss_store", embeddings=embedding, allow_dangerous_deserialization=True)

# Set up retriever and QA chain
retriever = db.as_retriever(search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key),
    retriever=retriever,
    return_source_documents=True
)

# Run a sample query
query = "Summarize issues reported by customers who recently churned"
print("🔍 Query:", query)

result = qa_chain({"query": query})
print("🧠 Answer:\n", result["result"])

print("\n📄 Source documents:")
for i, doc in enumerate(result["source_documents"]):
    print(f"--- Source {i+1} ---\n{doc.page_content[:200]}...\n")
