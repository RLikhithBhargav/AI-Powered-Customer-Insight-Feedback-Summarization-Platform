# File: app.py

import streamlit as st
import os
from dotenv import load_dotenv
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv(dotenv_path="../ai/creds.env")
openai_api_key = os.getenv("OPENAI_API_KEY")
embedding = OpenAIEmbeddings(openai_api_key=openai_api_key)

# Load FAISS vector store
@st.cache_resource
def load_vector_store():
    return FAISS.load_local("../ai/faiss_store", embeddings=embedding, allow_dangerous_deserialization=True)

db = load_vector_store()

custom_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant analyzing customer support feedback.

Based on the context below, identify recurring issues, themes, or complaints—even if they are indirectly stated or mentioned only once. Focus on extracting useful insights for product or support improvement.

If context is unclear or incomplete, make an educated guess based on tone and wording.

Context:
{context}

Question: {question}
Answer:"""
)

# Set up retrieval-based QA chain
retriever = db.as_retriever(search_kwargs={"k": 5})
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(model="gpt-4", openai_api_key=openai_api_key),
    retriever=retriever,
    return_source_documents=True,
    chain_type="stuff",  # Still fine for shorter context
    chain_type_kwargs={"prompt": custom_prompt}
)

# --- Streamlit UI ---
st.set_page_config(page_title="Customer Insights Agent", layout="wide")
st.title("🧠 Customer Feedback AI Agent")
st.markdown("Ask questions based on support tickets and feedback stored in your FAISS vector DB.")

query = st.text_input("💬 Ask a question:", placeholder="e.g. What do churned users in Texas complain about?")

if query:
    with st.spinner("Thinking..."):
        result = qa_chain({"query": query})

    st.markdown("### 🧠 Answer")
    st.success(result["result"])

    with st.expander("📄 View top 5 source documents"):
        for i, doc in enumerate(result["source_documents"]):
            st.markdown(f"**Source {i+1}:**")
            st.code(doc.page_content, language="text")
