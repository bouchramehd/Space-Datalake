# Space Data Lake

Projet Big Data basé sur les données astronomiques **Gaia DR3** et les données temps réel **NASA NeoWs**.

## Objectif du projet

L’objectif est de construire une architecture Data Lake permettant de gérer des données provenant de deux sources différentes :

- une source **Batch** : Gaia DR3 ;
- une source **Streaming** : NASA NeoWs.

Les principales technologies utilisées sont :

- Hadoop HDFS
- Apache Spark
- Apache Kafka
- Apache Airflow
- Docker
- Python
- Parquet

---

## Sources de données

### Gaia DR3 — Batch

Gaia DR3 constitue la source de données Batch du projet.

Les données sont téléchargées sous forme de fichiers CSV compressés.

- Source : Gaia DR3
- Type : Batch
- Format : CSV compressé (`.csv.gz`)
- Volume utilisé : environ **5,1 Go**

Les fichiers sont ensuite déposés dans la couche Bronze de HDFS :

```text
/bronze/source=gaia/year=2026/month=08/
```

---

### NASA NeoWs — Streaming

NASA NeoWs (**Near Earth Object Web Service**) fournit des informations concernant les objets géocroiseurs, notamment les astéroïdes proches de la Terre.

Les données sont récupérées depuis l’API NASA puis envoyées vers Kafka.

Flux de données :

```text
NASA NeoWs API
      ↓
    Kafka
      ↓
Spark Structured Streaming
      ↓
 HDFS Bronze
```

Le topic Kafka utilisé est :

```text
nasa-neows
```

Les données sont ensuite stockées dans :

```text
/bronze/source=neows/
```

---

# Architecture du Data Lake

L’architecture générale du projet est la suivante :

```text
                  SOURCES DE DONNÉES

             Gaia DR3        NASA NeoWs
                |                 |
                |                 v
                |               Kafka
                |                 |
                |                 v
                |        Spark Structured Streaming
                |                 |
                +--------+--------+
                         |
                         v
                      BRONZE
                         |
                       Spark
                         |
                         v
                      SILVER
                         |
                       Spark
                         |
                         v
                       GOLD

                    Apache Airflow
                         |
                  Orchestration
                  des traitements
```

---

# Organisation du Data Lake

Le Data Lake utilise une architecture en trois couches :

```text
BRONZE → SILVER → GOLD
```

## Couche Bronze

La couche Bronze contient les données brutes ou très peu transformées.

### Gaia

```text
/bronze/source=gaia/year=2026/month=08/
```

### NASA NeoWs

```text
/bronze/source=neows/year=2026/month=8/day=26/
```

La couche Bronze permet de conserver les données sources avant leur nettoyage.

---

## Couche Silver

La couche Silver contient les données nettoyées et structurées.

Les transformations réalisées avec Spark comprennent notamment :

- sélection des colonnes utiles ;
- conversion des types ;
- validation du schéma ;
- gestion des valeurs nulles ;
- suppression des doublons ;
- validation des données ;
- conversion au format Parquet.

### Gaia Silver

```text
/silver/source=gaia
```

### NeoWs Silver

```text
/silver/source=neows
```

---

## Couche Gold

La couche Gold contient les données finales préparées pour l’analyse.

Elle est construite à partir des données Silver et permet de produire des indicateurs, statistiques et agrégations exploitables pour l’analyse.

```text
Silver
   ↓
Spark
   ↓
Gold
   ↓
Analyse / KPIs
```

---

# Structure du projet

```text
space-datalake/
│
├── airflow/
│   └── dags/
│
├── data/
│   └── batch/
│       └── gaia/
│
├── scripts/
│   ├── download_gaia.py
│   └── nasa_producer.py
│
├── spark/
│   ├── bronze/
│   │   └── stream_neows.py
│   │
│   ├── silver/
│   │   ├── transform_gaia.py
│   │   └── transform_neows.py
│   │
│   └── gold/
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

# Infrastructure Docker

L’ensemble de l’environnement Big Data est déployé avec Docker Compose.

Les principaux services sont :

- **Kafka** : ingestion des données NASA en streaming ;
- **HDFS NameNode** : gestion du système de fichiers HDFS ;
- **HDFS DataNode** : stockage physique des données ;
- **Spark Master** : gestion du cluster Spark ;
- **Spark Worker** : exécution des traitements Spark ;
- **Airflow** : orchestration des différentes étapes du pipeline.

Pour démarrer l’environnement :

```bash
docker compose up -d
```

Pour vérifier les conteneurs :

```bash
docker ps
```

---

# Interfaces Web

## Spark

L’interface Spark permet de suivre les applications et les traitements exécutés.

```text
http://localhost:8080
```

## Hadoop HDFS

L’interface du NameNode permet de consulter l’état du cluster HDFS.

```text
http://localhost:9870
```

## Airflow

L’interface Airflow est disponible sur :

```text
http://localhost:8088
```

---

# Ingestion Batch Gaia

Les données Gaia sont téléchargées à l’aide du script :

```bash
python scripts/download_gaia.py
```

Environ **5,1 Go** de données Gaia ont été récupérés.

Les fichiers sont ensuite chargés dans HDFS dans la couche Bronze :

```text
/bronze/source=gaia/year=2026/month=08/
```

---

# Ingestion Streaming NASA NeoWs

Le producteur NASA peut être lancé avec :

```bash
python scripts/nasa_producer.py
```

Le script récupère les données depuis l’API NASA NeoWs et les transmet au topic Kafka :

```text
nasa-neows
```

Spark Structured Streaming consomme ensuite les événements Kafka et les enregistre dans HDFS au format Parquet.

Le flux est donc :

```text
NASA API → Kafka → Spark Streaming → HDFS Bronze
```

---

# Transformation Gaia Bronze → Silver

Les données Gaia présentes dans la couche Bronze sont traitées avec Apache Spark.

Le script utilisé est :

```text
spark/silver/transform_gaia.py
```

Le traitement permet de nettoyer et structurer les données avant leur écriture dans :

```text
/silver/source=gaia
```

---

# Gestion du code avec Git

Les données Gaia représentent plusieurs gigaoctets et ne doivent donc pas être envoyées sur Git.

Le fichier `.gitignore` permet notamment d’exclure :

```text
venv/
__pycache__/
*.pyc
.env
.vscode/
.idea/
*.log
data/batch/gaia/
```

Ainsi, seuls le code source, les scripts, la configuration Docker et la documentation sont versionnés.

---

# Technologies utilisées

- Python
- Apache Hadoop HDFS
- Apache Spark
- Spark Structured Streaming
- Apache Kafka
- Apache Airflow
- Docker / Docker Compose
- Parquet
- NASA NeoWs API
- Gaia DR3

---

# Pipeline global

```text
GAIA DR3
   |
   | Batch
   v
HDFS Bronze
   |
   v
Spark
   |
   v
HDFS Silver
   |
   v
Spark
   |
   v
HDFS Gold


NASA NeoWs API
   |
   v
Kafka
   |
   v
Spark Structured Streaming
   |
   v
HDFS Bronze
   |
   v
Spark
   |
   v
HDFS Silver
   |
   v
Spark
   |
   v
HDFS Gold
```

Apache Airflow est utilisé pour orchestrer les différentes étapes du pipeline.
