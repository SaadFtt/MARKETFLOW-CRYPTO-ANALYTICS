# MARKETFLOW CRYPTO ANALYTICS

A real-time cryptocurrency analytics pipeline using **Kafka, Spark, and PostgreSQL** on Ubuntu (WSL) via VS Code.  

---

## 🏗 Project Architecture

CoinGecko API
↓
Kafka Producer (crypto_dag.py)
↓
Kafka Topic: crypto-prices
↓
Spark Streaming (kafka_streaming.py)
↓
Parquet files
↓
Spark Analytics (analytics.py)
↓
PostgreSQL


- **Kafka Producer**: Fetches crypto prices from CoinGecko every 30s and pushes JSON messages to Kafka.  
- **Spark Streaming**: Reads from Kafka, processes streaming data, and writes Parquet files.  
- **Spark Analytics**: Performs analytics on Parquet files and stores results in PostgreSQL.  
- Fully integrated pipeline controlled by a **single master script**.  

---

## ⚙️ Setup Requirements

- Ubuntu via WSL (integrated with VS Code)  
- Python 3.12+  
- Kafka + Zookeeper  
- Spark  
- PostgreSQL  

---

## 📦 Python Dependencies

Install the required packages in a virtual environment:

```bash
python3 -m venv env
source env/bin/activate
pip install kafka-python requests pyspark psycopg2-binary


🚀 How to Run

Start services:

# Start Zookeeper
zookeeper-server-start.sh config/zookeeper.properties

# Start Kafka
kafka-server-start.sh config/server.properties

# Start PostgreSQL
sudo service postgresql start


Run the Kafka producer:

python crypto_dag.py


Pushes crypto prices to Kafka topic crypto-prices every 30s.

Run Spark streaming:

python kafka_streaming.py


Reads from Kafka, processes data, and writes Parquet files.

Run analytics:

python analytics.py

Reads Parquet files, performs analytics, and writes results to PostgreSQL.

✅ Notes

Airflow is NOT required for now — integration can come later.

The architecture is solid and coherent for a portfolio or real-world project.

Designed to run harmonically on WSL Ubuntu + VS Code.
