from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import docker


def exec_container(container_name, command):
    client = docker.from_env()
    container = client.containers.get(container_name)

    result = container.exec_run(command)

    output = result.output.decode("utf-8", errors="ignore")
    print(output)

    if result.exit_code != 0:
        raise RuntimeError(
            f"Command failed in {container_name}:\n{output}"
        )


def check_hdfs():
    exec_container(
        "namenode",
        ["hdfs", "dfsadmin", "-report"]
    )


def check_gaia_bronze():
    exec_container(
        "namenode",
        [
            "hdfs", "dfs", "-test", "-e",
            "/bronze/source=gaia/year=2026/month=08"
        ]
    )
    print("Gaia Bronze exists.")


def check_neows_bronze():
    exec_container(
        "namenode",
        [
            "hdfs", "dfs", "-test", "-e",
            "/bronze/source=neows"
        ]
    )
    print("NeoWs Bronze exists.")


with DAG(
    dag_id="ingestion_pipeline",
    description="Check Bronze data in HDFS",
    start_date=datetime(2026, 8, 27),
    schedule=None,
    catchup=False,
    tags=["space-datalake", "bronze"],
) as dag:

    hdfs = PythonOperator(
        task_id="check_hdfs",
        python_callable=check_hdfs
    )

    gaia = PythonOperator(
        task_id="check_gaia_bronze",
        python_callable=check_gaia_bronze
    )

    neows = PythonOperator(
        task_id="check_neows_bronze",
        python_callable=check_neows_bronze
    )

    hdfs >> [gaia, neows]