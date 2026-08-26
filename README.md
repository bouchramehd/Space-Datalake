# 🌌 Space Data Lakehouse

Projet Big Data basé sur des données astronomiques.

## Technologies

* Docker
* Kafka
* Spark
* HDFS
* Airflow
* Python
* Streamlit

## Data

* **Batch :** Gaia DR3 (~5 GB)
* **Temps réel :** NASA NeoWs API

## Installation

```bash
git clone <repository-url>
cd space-datalake
```

Créer l'environnement Python :

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Lancer Docker :

```bash
docker compose up -d
```

Télécharger les données Gaia :

```bash
python scripts/download_gaia.py
```

## Architecture

```text
Gaia DR3 ──────────────→ Bronze
                          ↓
NASA NeoWs → Kafka ────→ Bronze
                          ↓
                        Silver
                          ↓
                         Gold
                          ↓
                  Streamlit Dashboard

Airflow orchestre le pipeline.
```
