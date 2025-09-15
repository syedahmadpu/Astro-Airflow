# Automated ETL Pipeline for NASA's Astronomy Picture of the Day

This project demonstrates a complete, containerized ETL (Extract, Transform, Load) pipeline built with Apache Airflow. It automatically fetches the 'Astronomy Picture of the Day' (APOD) from a NASA API, processes the data, and loads it into a PostgreSQL database.

The entire development environment is managed by Docker and Docker Compose, making it easy to set up and run consistently.

## 🚀 Key Features
- **Automated Daily Extraction**: Schedules a daily run to fetch the latest data from the NASA APOD API.
- **Data Transformation**: Processes raw JSON data into a clean, structured format suitable for a relational database.
- **Containerized Environment**: Uses Docker and Docker Compose for a reproducible and isolated development setup, including Airflow and PostgreSQL services.
- **Secure Credential Management**: Leverages Airflow's built-in connection manager to securely store API keys and database passwords.
- **Cloud-Ready Architecture**: Designed with a cloud deployment strategy in mind (e.g., Astro Cloud for Airflow and AWS RDS for PostgreSQL).

## 📊 Architecture Flow
The pipeline follows a standard ETL process orchestrated by Airflow:

`NASA APOD API` → `Airflow (Extract)` → `Airflow (Transform)` → `Airflow (Load)` → `PostgreSQL Database`

## ⚙️ Technologies Used
- **Orchestration**: Apache Airflow (Hybrid DAGs, TaskFlow API, Operators, Hooks)
- **Containerization**: Docker, Docker Compose
- **Database**: PostgreSQL
- **Programming Language**: Python
- **Data Viewing**: DBeaver

## 📋 Setup and Configuration

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
- An API Key from [NASA API](https://api.nasa.gov/).
