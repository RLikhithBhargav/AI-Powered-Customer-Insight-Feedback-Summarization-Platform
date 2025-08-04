# 🧠 AI-Powered Customer Insight & Feedback Summarization Platform

> A full-stack data engineering and AI project combining cloud data pipelines, generative AI, vector-based search, interactive dashboards, and automated orchestration — designed to extract and surface actionable insights from customer behavior and support feedback data.

---

## 🚩 Problem Statement

Organizations collect vast amounts of customer data — from transaction logs to support tickets to feedback forms — yet struggle to convert that into timely, meaningful insights. This leads to reactive decisions, missed churn signals, and unstructured qualitative feedback going underutilized.

---

## 🎯 Objective

Build an end-to-end platform that:
- Ingests raw customer and feedback data
- Transforms it into analytics-ready tables using dbt
- Summarizes customer feedback using OpenAI GPT models
- Enables interactive exploration via a LangChain-powered chatbot
- Visualizes insights via an auto-refreshing dashboard
- Is fully orchestrated via Apache Airflow (Docker-based)

---

## 🧪 Dual Approach Breakdown

### 🧩 **Approach 1: Modular AI Stack**

| Layer             | Tools Used                     |
|------------------|--------------------------------|
| Storage          | Cloudtool S3 (local S3 wrapper) |
| Warehouse        | Snowflake                      |
| Transformation   | dbt                            |
| AI Summarization | OpenAI + LangChain + FAISS     |
| UI - Dashboard   | Streamlit                      |
| UI - Chatbot     | LangChain + GPT                |

→ Built for **modularity, experimentation, and exploration**  
→ The chatbot uses FAISS embeddings to search and summarize feedback interactively

---

### 🔁 **Approach 2: Automated Pipeline with Apache Airflow**

| Layer             | Tools Used                   |
|------------------|------------------------------|
| Orchestration    | Apache Airflow (Docker-based) |
| Ingestion        | Python Scripts               |
| Transformation   | dbt run inside DAG           |
| Summarization    | OpenAI API in DAG            |
| Export           | CSV for dashboard            |
| Monitoring       | Airflow UI logs              |

→ Built for **repeatability, automation, and end-to-end scheduling**

---

## ⚙️ Tech Stack

- **Python 3.10**
- **Snowflake**
- **Apache Airflow via Docker Desktop**
- **dbt-core**
- **OpenAI GPT-3.5/4**
- **LangChain + FAISS**
- **Streamlit**
- **Cloudtool S3** (for local S3 emulation)
- **Pandas, Altair, dotenv, tqdm**

---

## 🔄 End-to-End Workflow
📥 Step 1: Ingest Raw Data
- Load customer, transaction, support, and feedback data from local CSV or S3-like store

## 🏗️ Step 2: Transform via dbt
- Create fct_customer_features and fct_customer_behavior models in Snowflake

## ✨ Step 3: AI Summarization
- DAG version: uses OpenAI GPT-3.5 to summarize feedback statelessly
- Chatbot version: uses LangChain + FAISS for contextual exploration

## 📊 Step 4: Dashboard Refresh
- Streamlit dashboard refreshes automatically with updated customer_features.csv

## 🧠 Step 5: Interactive Chatbot (Optional)
- LangChain pipeline with FAISS lets users query the feedback vector DB

## 📦 Running Airflow via Docker
You’ll need:
- Docker Desktop installed and running
- Python 3.10 (outside of Docker)
- Your .env file with Snowflake and OpenAI credentials
  
## 🏃 Steps
```bash
cd airflow
docker-compose up airflow-init
docker-compose up
```
- Visit: http://localhost:8080
- Login: airflow / airflow
- Your DAG will appear as genai_customer_pipeline_dag

## 📊 Streamlit Dashboard
```bash
cd streamlit_dashboard
streamlit run app.py
```
Includes:
- Customer Churn Risk by Count
- Support Ticket Volume by Risk Category
- Avg Feedback Rating vs Churn Risk
- Drill-down tables per customer

## 💬 Example Chatbot Prompts
- “What are the recurring complaints from customers?”
- “Summarize what customers are saying about refunds.”
- “What are the most praised features in customer comments?”

(The chatbot uses LangChain + OpenAI + FAISS vector DB)

## 📌 Notes
- The dashboard and chatbot are intentionally decoupled from the DAG for modularity
- The OpenAI summaries in DAG are quick + stateless, suitable for automation
- The LangChain pipeline supports rich, real-time user queries using stored feedback vectors

## ✅ Conclusion
This project tackles the challenge of extracting actionable insights from scattered customer data by combining data engineering and generative AI. From raw ingestion to AI-driven feedback summaries and automated dashboards, it demonstrates a practical, scalable solution. By building both a modular stack and an orchestrated pipeline, I was able to explore and showcase two distinct yet complementary approaches to solving this real-world problem.
