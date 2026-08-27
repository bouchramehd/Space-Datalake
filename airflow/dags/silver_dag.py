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


def transform_gaia():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "/opt/spark-apps/silver/transform_gaia.py"
        ]
    )


def transform_neows():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "/opt/spark-apps/silver/transform_neows.py"
        ]
    )


with DAG(
    dag_id="silver_pipeline",
    description="Bronze to Silver with Spark",
    start_date=datetime(2026, 8, 27),
    schedule=None,
    catchup=False,
    tags=["space-datalake", "silver"],
) as dag:

    gaia_silver = PythonOperator(
        task_id="gaia_bronze_to_silver",
        python_callable=transform_gaia
    )

    neows_silver = PythonOperator(
        task_id="neows_bronze_to_silver",
        python_callable=transform_neows
    )

    [gaia_silver, neows_silver]