# ML + LLM Pipeline Orchestration 🦾🤖

[![Python](https://img.shields.io/badge/Python-3.10-blue?logo=python)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-20.10+-blue?logo=docker)](https://www.docker.com/)
[![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.8.2-blue?logo=apacheairflow)](https://airflow.apache.org/)
[![MLflow](https://img.shields.io/badge/MLflow-2.11.3-blue?logo=mlflow)](https://mlflow.org/)
[![Spark](https://img.shields.io/badge/Spark-4.0.0-orange?logo=apachespark)](https://spark.apache.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110.1-green?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-black?logo=flask)](https://flask.palletsprojects.com/)
[![Sentence Transformers](https://img.shields.io/badge/SentenceTransformers-2.6.1-blue)](https://www.sbert.net/)
[![pandas](https://img.shields.io/badge/Pandas-2.2.2-blue?logo=pandas)](https://pandas.pydata.org/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.4.2-blue?logo=scikit-learn)](https://scikit-learn.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0.3-blue?logo=xgboost)](https://xgboost.readthedocs.io/)
[![FAISS](https://img.shields.io/badge/FAISS-1.7.4-blue)](https://github.com/facebookresearch/faiss)
[![pdfplumber](https://img.shields.io/badge/pdfplumber-0.11.0-blue)](https://github.com/jsvine/pdfplumber)

---

## ▶️ Demo Videos

- [**Demo Video 1: Full ML + LLM Pipeline Orchestration**](https://drive.google.com/file/d/1R6i-6w9v-OTSZvobLzKbAg9LpDRmQ9bB/view?usp=drive_link)
- [**Demo Video 2: RAG Service Query Demo**](https://drive.google.com/file/d/1MxvYbs7p1eOF0BvVB2xuGwEnrwSeXqFq/view?usp=drive_link)

---

## 📖 Table of Contents

- [📌 Introduction](#-introduction)
- [🗺️ Architecture Overview](#-architecture-overview)
- [🎯 Mermaid Diagram](#-mermaid-diagram)
- [▶️ Demo Videos](#️-demo-videos)
- [🛠️ Technology Stack](#-technology-stack)
- [🚀 Setup and Installation](#-setup-and-installation)
  - [1️⃣ Prerequisites](#1-prerequisites)
  - [2️⃣ Python Installation](#2-python-installation)
  - [3️⃣ Docker Installation](#3-docker-installation)
  - [4️⃣ Docker Compose Installation (If Required)](#4-docker-compose-installation-if-required)
  - [5️⃣ Clone the Repository](#5-clone-the-repository)
  - [6️⃣ Project Structure](#6-project-structure)
  - [7️⃣ Python Virtual Environment (Optional)](#7-python-virtual-environment-optional)
  - [8️⃣ Environment Variables and Configuration](#8-environment-variables-and-configuration)
- [⚒️ How to Build and Run the Project](#️-how-to-build-and-run-the-project)
- [🌐 Service Endpoints](#-service-endpoints)
- [🛠️ Airflow Troubleshooting](#️-airflow-troubleshooting)
- [💡 MLflow Troubleshooting](#-mlflow-troubleshooting)
- [🔗 Pipeline DAG (Mermaid Diagram)](#-pipeline-dag-mermaid-diagram)
- [🔍 How Each Service Works](#-how-each-service-works)
- [🐞 Common Issues and Solutions](#-common-issues-and-solutions)
- [🚦 Advanced Usage](#-advanced-usage)
- [🚀 Using the RAG Services UI (Swagger UI, Postman, or API Client)](#-using-the-rag-services-ui-swagger-ui-postman-or-api-client-)
  - [🗂️ Step 1: Switch Context (Choose Dataset)](#-step-1-switch-context-choose-dataset)
  - [📥 Step 2: Ingest Your Dataset (CSV)](#-step-2-ingest-your-dataset-csv)
  - [💬 Step 3: Ask Questions (`/rag_query`)](#-step-3-ask-questions-rag_query)
- [🧪 Sample Questions to Test in RAG Services UI](#-sample-questions-to-test-in-rag-services-ui)
- [🏆 Best Practices & Pro Tips](#-best-practices--pro-tips)
- [🗂️ RAG Services UI Workflow Recap](#-rag-services-ui-workflow-recap)
- [📝 Appendix: Example Commands & API Requests](#-appendix-example-commands--api-requests)
- [✨ FAQ](#-faq)
- [⚖️ License](#-license)
- [👤 Contact](#-contact)

---

## 📌 Introduction

> **ML + LLM Pipeline Orchestration** is a robust, scalable, and modular system for orchestrating end-to-end machine learning (ML) and retrieval-augmented generation (RAG) workflows. It leverages containerization, modern orchestration, and state-of-the-art ML/RAG techniques for production-ready deployment and reproducibility.

**Key Features:**
- 🔁 Orchestrates the ML workflows using Apache Airflow (ETL, training, evaluation, and tracking)
- ⚡ ML model training, evaluation, tracking, and API serving
- 🤖 RAG API for LLM workflows with vector search and context retrieval
- 📊 Experiment tracking via MLflow
- 🖥️ Distributed data processing using Apache Spark
- 🐳 Fully containerized for easy deployment and reproducibility

---

## 🗺️ Architecture Overview

<!--
All major services are decoupled and run in their own containers.
Data flows via shared volumes and REST APIs.
Airflow orchestrates the ML pipeline steps.
RAG and ML services are API endpoints for LLM and ML workflows.
-->

- **Airflow** triggers all pipeline steps and schedules periodic tasks.
- **ML pipeline** handles preprocessing, feature engineering, training, and evaluation.
- **MLflow** logs metrics and models for experiment tracking.
- **ML Service** provides APIs for serving ML models.
- **RAG Service** exposes APIs for LLMs and context retrieval.
- **Spark** enables distributed computation for data preprocessing.
- **Shared data** is managed by Docker volumes and accessible by all containers.

---

## 🎯 Mermaid Diagram

```mermaid
flowchart TD
    subgraph Data_Processing
        Spark["⚡ Spark Master"]
        Preprocess["🧹 Preprocess.py"]
        FeatureEng["🛠️ Feature Engineering.py"]
    end

    subgraph ML_Training
        Train["🏋️ Train.py"]
        Evaluate["🧪 Evaluate.py"]
        MLflow["📊 MLflow Tracking"]
    end

    subgraph Services
        MLService["🧠 ML Service (Flask)"]
        RAGService["🤖 RAG Service (FastAPI)"]
    end

    Data["🗂️ Data"]
    Airflow -->|Triggers| Preprocess
    Preprocess --> FeatureEng
    FeatureEng --> Train
    Train --> Evaluate
    Train --> MLflow
    Evaluate --> MLflow
    MLService <-->|API| MLflow
    RAGService <-->|API| MLService
    Spark <--> Preprocess
    Spark <--> FeatureEng
    Data -.->|Shared| Preprocess
    Data -.->|Shared| FeatureEng
    Data -.->|Shared| Train
    Data -.->|Shared| Evaluate
    Data -.->|Shared| RAGService
```


---

## 🛠️ Technology Stack

- **🐍 Python 3.10** — All custom scripts/services
- **🐳 Docker** — Containerization of all services
- **🍱 Docker Compose** — Multi-container orchestration
- **🌀 Apache Airflow** — Workflow orchestration and scheduling
- **📈 MLflow** — ML experiment tracking/model registry
- **⚡ Apache Spark** — Distributed preprocessing (**used for data preprocessing and feature engineering in Airflow DAGs**)
- **⚡ FastAPI** — Modern, fast web framework for RAG Service
- **🧠 Flask** — Lightweight web framework for ML Service
- **🔤 Sentence Transformers** — Text embedding for RAG
- **🗃️ FAISS** — Fast vector similarity search/indexing
- **📊 pandas, scikit-learn, XGBoost** — ML stack
- **📄 pdfplumber** — PDF ingestion

---

## 🚀 Setup and Installation

### 1️⃣ Prerequisites

You need the following on your system:

- **Git**: For cloning the repository  
- **Python 3.10+**: For local scripts and Docker images  
- **Docker (20.10+)**: For containerization  
- **Docker Compose**: Included in most Docker Desktop installations  

---

### 2️⃣ Python Installation

> **You only need Python installed on your host if you want to run scripts or tests locally (not inside Docker).**

#### 🪟 Windows

1. Download Python from [python.org](https://www.python.org/downloads/).
2. Run the installer and **check "Add Python to PATH"**.
3. Verify installation:
   ```sh
   python --version
   ```

#### 🍏 macOS

1. Install Homebrew (if not installed):
   ```sh
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install Python:
   ```sh
   brew install python@3.10
   python3 --version
   ```

#### 🐧 Linux (Ubuntu/Debian)

```sh
sudo apt-get update
sudo apt-get install python3.10 python3.10-venv python3.10-dev -y
python3.10 --version
```

---

### 3️⃣ Docker Installation

**🪟 Windows:**  
- Download Docker Desktop: [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop)
- Follow installer prompts, start Docker Desktop, and verify:
  ```sh
  docker --version
  ```

**🍏 macOS:**  
- Download Docker Desktop: [Docker Desktop for Mac](https://www.docker.com/products/docker-desktop)
- Drag Docker to Applications, start Docker Desktop, and verify:
  ```sh
  docker --version
  ```

**🐧 Linux (Ubuntu/Debian):**
```sh
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | \
    sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
  "deb [arch="$(dpkg --print-architecture)" \
  signed-by=/etc/apt/keyrings/docker.gpg] \
  https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
sudo usermod -aG docker $USER
docker --version
```

---

### 4️⃣ Docker Compose Installation (If Required)

**Most Docker Desktop installations include Compose.**

**🐧 Linux:**  
```sh
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.7/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

---

### 5️⃣ Clone the Repository

```sh
git clone https://github.com/Pavansai20054/AI-Backend-Hiring-Tasks-Prodigal-AI.git

cd "AI-Backend-Hiring-Tasks-Prodigal-AI/Task 1 - ML + LLM Pipeline Orchestration"
```

---

## 6️⃣ Project Structure 🗂️✨

> **💡 Each directory/service has a clear responsibility.**

```
.
├── airflow/                             # 🌀 Airflow orchestration
│   └── dags/                            # 📅 DAGs for ML pipelines
│       ├── ml_pipeline_titanic_dag.py       # 🚢 Titanic pipeline DAG
│       └── ml_pipeline_winequality_dag.py   # 🍷 Wine Quality pipeline DAG
├── data/                                # 📊 Datasets
│   ├── titanic.csv                          # 🚢 Titanic dataset
│   └── winequality-red.csv                  # 🍷 Wine Quality dataset
├── mlruns/                              # 🗃️ MLflow experiment storage (auto-generated)
├── ml_pipeline/                         # 🏗️ ML scripts
│   ├── serve.py                             # 🌐 Serve ML model API
│   ├── titanic_evaluate.py                  # 🧪 Titanic evaluation
│   ├── titanic_feature_engineering.py       # 🛠️ Titanic feature engineering
│   ├── titanic_preprocess.py                # 🧹 Titanic data preprocessing
│   ├── titanic_train.py                     # 🏋️ Titanic model training
│   ├── wine_evaluate.py                     # 🧪 Wine evaluation
│   ├── wine_feature_engineering.py          # 🛠️ Wine feature engineering
│   ├── wine_preprocess.py                   # 🧹 Wine data preprocessing
│   └── wine_train.py                        # 🏋️ Wine model training
├── rag_pipeline/                        # 🧠 RAG (Retrieval-Augmented Generation) scripts
│   ├── embed.py                             # 🔤 Embedding utility
│   ├── ingest.py                            # 📥 Ingest data for RAG
│   ├── rag_api.py                           # 🤖 RAG API service
│   └── vector_store.py                      # 🗄️ Vector store (FAISS)
├── docker-compose.yml                   # 🐳 Docker Compose config
├── Dockerfile.airflow                   # 🌀 Airflow Dockerfile
├── Dockerfile.ml                        # 🏗️ ML Service Dockerfile
├── Dockerfile.rag                       # 🤖 RAG Service Dockerfile
├── Makefile                             # 🛠️ Makefile for easy commands
├── README.md                            # 📖 This documentation
├── requirements.txt                     # 📦 Python dependencies
└── todo.md                              # ✅ Project TODOs
```

---

### 7️⃣ Python Virtual Environment (Optional)

For running scripts locally (not required for Docker):

```sh
python3.10 -m venv prodigal_env
source prodigal_env/bin/activate  # (Linux/macOS)
prodigal_env\Scripts\activate     # (Windows)
pip install -r requirements.txt
```

---

### 8️⃣ Environment Variables and Configuration

- All main configs are in `docker-compose.yml`.
- Volumes are used to persist data across runs.
- To customize DB URIs, edit environment in Compose file.

---

## ⚒️ How to Build and Run the Project 🚦

> **Each step is important! Follow in order for smooth setup.**

---

### 0️⃣ (Optional, but Recommended) Start with a Clean Slate 🧹

If you want to **wipe all Docker images, containers, and volumes, and clean your MLflow experiments**, follow these steps:

#### 🪟 Windows (PowerShell):

```powershell
# Remove old mlruns directory (MLflow experiment data)
Remove-Item -Recurse -Force .\mlruns

# Re-create a clean mlruns directory (ensures Docker can write)
New-Item -ItemType Directory -Path .\mlruns

# Grant full permissions to mlruns directory (avoids Docker permission errors)
icacls .\mlruns /grant "Everyone:(F)" /T

# Stop and remove all running containers, networks, and named volumes from compose
docker compose down -v

# Remove all Docker images, containers, volumes, and build cache
docker system prune -a -f --volumes
```

#### 🐧 Linux/macOS (Terminal):

```sh
rm -rf ./mlruns                 # Remove previous MLflow experiment data
mkdir ./mlruns                  # Re-create mlruns directory
chmod -R 777 ./mlruns           # Ensure Docker has permissions
docker compose down -v          # Stop and remove containers, volumes
docker system prune -a -f --volumes  # Remove all images/volumes
```

> 💡 **Use these commands only when you want to fully reset your environment! This will remove all containers, images, and saved model/data volumes.**

---

### 1️⃣ Build Docker Images 🏗️

```sh
docker-compose build
```
or with Makefile:
```sh
make build
```

---

### 2️⃣ Initialize Airflow Database 🚦

> **Do this ONLY once, after first build or after deleting volumes.**

```sh
docker-compose run airflow airflow db init
```
or:
```sh
make airflow-init
```

---

### 3️⃣ Start All Services 🚀

```sh
docker-compose up
```
or:
```sh
make up
```

To run in the background:
```sh
docker-compose up -d
```

---

### 4️⃣ Stopping All Services 🛑

```sh
docker-compose down
```
or:
```sh
make down
```

---

### 5️⃣ Clean Up All Volumes & Images 🧹

```sh
docker-compose down -v --rmi all
```
or, to also prune dangling images/volumes:
```sh
docker system prune -a -f --volumes
```

---

## 🌐 Service Endpoints 🌎

| Service         | URL                                    | Description                          |
|-----------------|----------------------------------------|--------------------------------------|
| 🌀 Airflow         | http://localhost:8081                  | Airflow UI (admin/admin)             |
| 📈 MLflow         | http://localhost:5000                  | MLflow Tracking UI                   |
| 🧠 ML Service     | http://localhost:5001                  | Flask ML API root                    |
| 🤖 RAG Service    | http://localhost:8000                  | FastAPI RAG root (404 normal)        |
| 📓 RAG Swagger UI | http://localhost:8000/docs             | FastAPI docs                         |
| ⚡ Spark Master UI| http://localhost:8080                  | Spark Web UI                         |

---

## 🌀 How to Use Airflow & Where Spark Is Used

After starting all services, open the **Airflow UI** at [http://localhost:8081](http://localhost:8081) and log in with:

- **Username:** `admin`
- **Password:** `admin`

### To Run the ML + LLM Pipeline via Airflow:

1. **Find the DAG** you want to run (e.g., `ml_pipeline_titanic` or `ml_pipeline_winequality`).
2. **Click the play button (▶️)** next to the DAG name to trigger the pipeline.
3. The DAG will automatically execute all pipeline steps in order:
   - **Preprocessing (Spark job)** — Uses Spark for distributed data cleaning and filling missing values.
   - **Feature Engineering (Spark job)** — Uses Spark for encoding, splitting, and saving features.
   - **Model Training** — Runs in Python (scikit-learn/XGBoost).
   - **Model Evaluation** — Runs in Python and logs metrics to MLflow.
4. **Monitor progress** in Airflow's UI (Graph View, Tree View, Logs, etc.).
5. **View experiment results** in MLflow UI at [http://localhost:5000](http://localhost:5000).

> **Spark is used in the pipeline for the preprocessing and feature engineering steps, ensuring distributed and scalable data handling. These are triggered via Airflow BashOperator tasks running the relevant Spark/PySpark scripts.**

---

## 🔗 Pipeline DAG (Mermaid Diagram) 📊

```mermaid
graph TD;
    A[🧹 Preprocess Data] --> B[🛠️ Feature Engineering]
    B --> C[🏋️ Train Model]
    C --> D[🧪 Evaluate Model]
    C --> E[📦 Log Model to MLflow]
    D --> E
    E --> F[🧠 ML Service API]
    F --> G[🤖 RAG Service API]
    subgraph Orchestrator
      A
      B
      C
      D
    end
    subgraph Services
      F
      G
    end
```

---

## 🔍 How Each Service Works 🧩

### 🌀 Airflow

- Orchestrates the entire ML pipeline via DAGs.
- Triggers Python scripts for ETL, training, and evaluation.
- Handles scheduling and monitoring.

### 🧠 ML Service

- Flask API serving model predictions.
- Healthcheck endpoint at `/`.
- Communicates with MLflow for model artifacts.

### 🤖 RAG Service

> RAG Services will automatically turn off after 5 to 10 minutes because of heavy model being used from hugging face
- FastAPI backend for retrieval-augmented generation.
- Embeds, indexes, and serves context for LLM queries.
- `/docs` endpoint gives OpenAPI UI for testing.
- Uses Sentence Transformers and FAISS for vector search.

### 📈 MLflow

- Tracks experiment runs, metrics, models.
- UI at http://localhost:5000

### ⚡ Spark

- Used for distributed ETL/preprocessing in Airflow DAGs.
- UI at http://localhost:8080

---

## 🐞 Common Issues and Solutions 🛠️

### 1. "Endpoint not found" for ML/RAG Service

- **Cause:** Accessing `/` on RAG service (which only has `/docs`, `/rag_query`)
- **Solution:** Use `/docs` or POST to `/rag_query`.

### 2. "Database not initialized" (Airflow)

- **Cause:** Airflow DB not persisted via volume.
- **Solution:** See [Airflow Troubleshooting](#️-airflow-troubleshooting).

### 3. "Permission denied" on volumes

- **Cause:** Docker container cannot write to mapped host folders.
- **Solution:** Change directory permissions on host.

### 4. "Image not found" Errors

- **Cause:** Docker images not built.
- **Solution:**  
  ```sh
  docker-compose build
  ```

### 5. "Port already allocated"

- **Cause:** Port in use.
- **Solution:** Change port mapping in `docker-compose.yml` or stop the other service.

---

## 🚦 Advanced Usage ⚙️

### 🔹 Running Airflow CLI

```sh
docker-compose run airflow airflow dags list
docker-compose run airflow airflow tasks list ml_pipeline_dag
```

### 🔹 Customizing the Pipeline

- Add/modify scripts in `ml_pipeline` or `rag_pipeline`.
- Update Airflow DAGs in `airflow/dags`.

### 🔹 Logs

```sh
docker-compose logs airflow
docker-compose logs ml_service
docker-compose logs rag_service
docker-compose logs mlflow
```

### 🔹 Clean Up

```sh
docker-compose down -v --rmi all
```
or:
```sh
docker system prune -a -f --volumes
```

---

## 🚀 Using the RAG Services UI (Swagger UI, Postman, or API Client) 🤖🦾

The RAG Service exposes a powerful API for question-answering and document ingestion. Here’s how to interact with the service directly (not using the Demo UI):

### 🗂️ Step 1: Switch Context (Choose Dataset)

1. Go to [RAG Swagger UI](http://localhost:8000/docs) or use any API client (like Postman).
2. Use the `POST /switch_context` endpoint.
3. Example request body for Titanic:
   ```json
   {
     "dataset": "titanic"
   }
   ```
   Example for Wine:
   ```json
   {
     "dataset": "wine"
   }
   ```
4. ✅ Wait for the success message. Always switch context before uploading or querying to ensure you’re working with the right dataset!

---

### 📥 Step 2: Ingest Your Dataset (CSV)

1. Use `POST /ingest_csv` to upload your dataset file (e.g., `titanic.csv` or `winequality-red.csv`).
2. In Swagger UI, click "Try it out", then select your file and execute.
3. You should receive a response with `status: success`, the filename, chunk count, and the active dataset.
4. 🟢 **Tip:** Re-ingest if you update your dataset!

---

### 💬 Step 3: Ask Questions (`/rag_query`)

1. Use `POST /rag_query` for natural language queries.
2. Example request body:
   ```json
   {
     "query": "Who had a higher chance of survival: males or females?",
     "top_k": 3
   }
   ```
3. The response will include:
   - The synthesized answer (from the model/context).
   - The top K context items used.
   - Dataset information and context count.

---

## 🧪 Sample Questions to Test in RAG Services UI

### 🚢 Titanic Dataset

- "Who had a higher chance of survival: males or females?"
- "How does age affect the survival rate in the Titanic dataset?"
- "What does the 'Pclass' column represent?"
- "List the possible values for 'Embarked' and their meanings."
- "What is the meaning of the 'Fare' column?"
- "What is the range of ages for Titanic passengers?"
- "Explain the significance of the 'SibSp' column."
- "Give a summary of the Titanic dataset."
- "What are the most important factors for survival?"
- "Who were more likely to survive: children or adults?"

### 🍷 Wine Quality Dataset

- "What affects wine quality most in the dataset?"
- "What does 'residual sugar' mean in the wine dataset?"
- "How does alcohol content relate to wine quality?"
- "What is the typical range of pH values in the dataset?"
- "Describe the meaning of the 'sulphates' column."
- "What is the range of 'chlorides' values in the data?"
- "Which features are most associated with high quality wines?"
- "What is the meaning of 'density' in the wine dataset?"
- "How many unique values are there in the 'quality' column?"
- "Which variable shows the greatest variation across samples?"

---

## 🏆 Best Practices & Pro Tips

- 🔄 **Always switch context** before any new dataset operation (upload, query).
- 📥 **Ingest your CSV** after switching or updating datasets.
- 💡 **Ask clear, specific questions** for best results.
- 🧠 **Try both analytical and definitional questions** to see the full power of the RAG system.
- 🔍 **If you get "not available" answers**, check that your data and schema are well-ingested and try adding more context or rephrasing your query.
- 📝 **Use the Swagger UI's "Try it out" for quick testing** or use Postman/cURL for automation.

---

## 🗂️ RAG Services UI Workflow Recap

| Step             | Action                             | Endpoint               | Example/Tip                                             |
|------------------|------------------------------------|------------------------|---------------------------------------------------------|
| Switch Context   | Choose Titanic or Wine dataset     | POST `/switch_context` | `{ "dataset": "titanic" }` or `{ "dataset": "wine" }`   |
| Ingest CSV       | Upload the dataset file            | POST `/ingest_csv`     | Use "Try it out" or Postman to upload                   |
| Query RAG        | Ask your question                  | POST `/rag_query`      | See sample questions above                              |

---

## 📝 Appendix: Example Commands & API Requests

```sh
# Test RAG API
curl -X POST "http://localhost:8000/rag_query" \
     -H "Content-Type: application/json" \
     -d "{\"query\": \"What is the Eiffel Tower?\"}"

# Airflow DAG Trigger
# 1. Open http://localhost:8081
# 2. Login with admin/admin
# 3. Find and trigger ml_pipeline_dag

# Rebuild ML Service after code changes
docker-compose build ml_service
docker-compose up ml_service

# Access logs for debugging
docker-compose logs airflow
docker-compose logs ml_service
docker-compose logs rag_service
docker-compose logs mlflow
```

---

## ✨ FAQ

**Q: Can I use a different database for Airflow/MLflow?**  
A: Yes, update the database URI in `docker-compose.yml` and ensure the service can access the new DB.

**Q: I get "cannot connect" errors for a service.**  
A: Wait for all containers to start (Airflow and MLflow may take 1-2 min on first startup).

**Q: Can I change host ports?**  
A: Yes, edit the port mappings in `docker-compose.yml`.

**Q: How do I update dependencies?**  
A: Edit `requirements.txt` and rebuild affected services with `docker-compose build`.

---

## ⚖️ License 📜

> 🛑 **This project is _not open source_. All rights reserved.**

See the [LICENSE](../../LICENSE) file for details.

---

## 👤 Contact 🙋

**Pavan Sai** 👨‍💻

📧 **Email**: [pavansai7654321@gmail.com](mailto:pavansai7654321@gmail.com)  
🐙 **GitHub**: [@Pavansai20054](https://github.com/Pavansai20054)  