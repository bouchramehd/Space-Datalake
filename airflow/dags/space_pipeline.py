from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
from datetime import datetime
import docker


# ============================================================
# COMMON FUNCTION
# ============================================================

def exec_container(container_name, command):
    """
    Execute a command inside an existing Docker container.
    Airflow uses this function to communicate with HDFS and Spark.
    """

    client = docker.from_env()
    container = client.containers.get(container_name)

    result = container.exec_run(command)

    output = result.output.decode("utf-8", errors="ignore")
    print(output)

    if result.exit_code != 0:
        raise RuntimeError(
            f"Command failed in container {container_name}:\n{output}"
        )


# ============================================================
# BRONZE / INGESTION
# ============================================================

def check_hdfs():
    exec_container(
        "namenode",
        [
            "hdfs",
            "dfsadmin",
            "-report"
        ]
    )


def check_gaia_bronze():
    exec_container(
        "namenode",
        [
            "hdfs",
            "dfs",
            "-test",
            "-e",
            "/bronze/source=gaia/year=2026/month=08"
        ]
    )

    print("Gaia Bronze exists.")


def check_neows_bronze():
    exec_container(
        "namenode",
        [
            "hdfs",
            "dfs",
            "-test",
            "-e",
            "/bronze/source=neows"
        ]
    )

    print("NeoWs Bronze exists.")


# ============================================================
# SILVER
# ============================================================

def transform_gaia_silver():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master",
            "spark://spark-master:7077",
            "/opt/spark-apps/silver/transform_gaia.py"
        ]
    )


def transform_neows_silver():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master",
            "spark://spark-master:7077",
            "/opt/spark-apps/silver/transform_neows.py"
        ]
    )


# ============================================================
# GOLD
# ============================================================

def transform_gaia_gold():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master",
            "spark://spark-master:7077",
            "/opt/spark-apps/gold/gaia_kpis.py"
        ]
    )


def transform_neows_gold():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master",
            "spark://spark-master:7077",
            "/opt/spark-apps/gold/neows_kpis.py"
        ]
    )


# ============================================================
# AIRFLOW DAG
# ============================================================

with DAG(
    dag_id="space_datalake_pipeline",
    description="Complete Space Data Lake pipeline: Bronze -> Silver -> Gold",
    start_date=datetime(2026, 8, 27),
    schedule=None,
    catchup=False,
    tags=["space-datalake", "gaia", "neows"],
) as dag:

    # ========================================================
    # BRONZE
    # ========================================================

    with TaskGroup(
        group_id="bronze",
        tooltip="Validate Bronze data in HDFS"
    ) as bronze:

        hdfs = PythonOperator(
            task_id="check_hdfs",
            python_callable=check_hdfs
        )

        gaia_bronze = PythonOperator(
            task_id="check_gaia",
            python_callable=check_gaia_bronze
        )

        neows_bronze = PythonOperator(
            task_id="check_neows",
            python_callable=check_neows_bronze
        )

        hdfs >> [gaia_bronze, neows_bronze]

    # ========================================================
    # SILVER
    # ========================================================

    with TaskGroup(
        group_id="silver",
        tooltip="Bronze to Silver transformations"
    ) as silver:

        gaia_silver = PythonOperator(
            task_id="gaia_bronze_to_silver",
            python_callable=transform_gaia_silver
        )

        neows_silver = PythonOperator(
            task_id="neows_bronze_to_silver",
            python_callable=transform_neows_silver
        )

    # ========================================================
    # GOLD
    # ========================================================

    with TaskGroup(
        group_id="gold",
        tooltip="Silver to Gold KPI generation"
    ) as gold:

        gaia_gold = PythonOperator(
            task_id="gaia_silver_to_gold",
            python_callable=transform_gaia_gold
        )

        neows_gold = PythonOperator(
            task_id="neows_silver_to_gold",
            python_callable=transform_neows_gold
        )

    # ========================================================
    # PIPELINE DEPENDENCIES
    # ========================================================

    bronze >> silver >> gold