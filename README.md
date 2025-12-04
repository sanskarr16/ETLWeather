# ☁️ ETL Weather Data Pipeline (Airflow + Postgres + Docker)

This project implements a complete **ETL (Extract, Transform, Load) Data Pipeline** using **Apache Airflow**, **PostgreSQL**, and **Docker (Astronomer Platform)**.  
It automatically fetches real-time weather data from the **Open-Meteo API**, transforms the response, and loads it into a PostgreSQL database.

The pipeline runs every day and is fully automated.

---

## 📌 **Features**
- ✔️ Extract weather data from Open-Meteo API  
- ✔️ Transform and clean the JSON response  
- ✔️ Load structured data into PostgreSQL  
- ✔️ Apache Airflow DAG orchestration  
- ✔️ Runs fully inside Docker using Astronomer  
- ✔️ Daily scheduled pipeline  
- ✔️ Tested and successfully executed  
- ✔️ Easy to extend and scale  

---

## 🛠️ **Tech Stack**
| Component | Technology |
|----------|------------|
| Orchestration | Apache Airflow |
| Database | PostgreSQL |
| Infrastructure | Docker + Astronomer |
| Language | Python |
| API Source | Open-Meteo Weather API |
| Airflow Hooks Used | HttpHook, PostgresHook |

---
## Folder Structure
```plaintext
ETLWeather/
│── dags/
│   └── etlweather.py          # Main ETL DAG
│── docker-compose.yml         # Docker services for Airflow + Postgres
│── Dockerfile                 # Custom Airflow image build
│── requirements.txt           # Python dependencies
│── include/
│── plugins/
│── packages.txt
│── .env
│── README.md
```
## Run the Project Using Docker (Astronomer)
Start Airflow + Postgres
astro dev start

You will see:

Airflow UI: http://localhost:8080
Postgres: postgresql://localhost:5432/postgres
Credentials: postgres / postgres

## 🔌 Required Airflow Connections
✔ Postgres Connection

Conn ID: postgres_default
Conn Type: Postgres
Host: postgres
Port: 5432
User: postgres
Password: postgres
Database: postgres

## ✔ Weather API Connection
Conn ID: open_meteo_api
Conn Type: HTTP
Host: https://api.open-meteo.com
Extra: {}

## Project Screenshots
<img width="1919" height="1079" alt="Screenshot 2025-12-04 084632" src="https://github.com/user-attachments/assets/0f9f84fc-f60b-4ca1-bf05-8f80f9123c51" />
<img width="1919" height="1079" alt="Screenshot 2025-12-04 084702" src="https://github.com/user-attachments/assets/7d04f50d-8aed-4376-a2a3-80f0d2853547" />
<img width="1919" height="1079" alt="Screenshot 2025-12-04 084743" src="https://github.com/user-attachments/assets/044d231d-7017-4baf-94e1-7fffaef863ba" />






## 📂 **Project Structure**
