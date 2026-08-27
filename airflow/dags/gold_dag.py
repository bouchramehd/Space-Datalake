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


def build_gaia_gold():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "/opt/spark-apps/gold/gaia_kpis.py"
        ]
    )


def build_neows_gold():
    exec_container(
        "spark-master",
        [
            "spark-submit",
            "--master", "spark://spark-master:7077",
            "/opt/spark-apps/gold/neows_kpis.py"
        ]
    )


with DAG(
    dag_id="gold_pipeline",
    description="Silver to Gold with Spark",
    start_date=datetime(2026, 8, 27),
    schedule=None,
    catchup=False,
    tags=["space-datalake", "gold"],
) as dag:

    gaia_gold = PythonOperator(
        task_id="gaia_silver_to_gold",
        python_callable=build_gaia_gold
    )

    neows_gold = PythonOperator(
        task_id="neows_silver_to_gold",
        python_callable=build_neows_gold
    )

    [gaia_gold, neows_gold]