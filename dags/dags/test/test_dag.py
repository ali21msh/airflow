import datetime

from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator

PIPELINE_NAME = "test-pipeline"
IMAGE = "data-metro:latest"
APPLICATION_ARGS = {
    "GIT_URL": "https://git.routerhosting.com",
    "GIT_ACCESS_TOKEN": "glpat-rXTZKMAxZsKkwpyntYpy",
    "PIPELINE_PATH": "pipeline.yml",
    "GIT_REPO_ID": 115,
    "PROFILE": "production",
}

default_args = {
    'owner': 'Ali Mashhadi',
    'depends_on_past': False,
    'start_date': '2024-01-03',
    'email': ['ali_mashhadi78@outlook.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': datetime.timedelta(minutes=5)
}

with DAG(
        dag_id=PIPELINE_NAME,
        default_args=default_args,
        schedule="0 */1 * * *",
        max_active_runs=1,
        catchup=False,
        concurrency=10
) as dag:
    DockerOperator(
        dag=dag,
        task_id=PIPELINE_NAME,
        image=IMAGE,
        container_name=PIPELINE_NAME,
        api_version="auto",
        auto_remove='force',
        docker_url='unix://var/run/docker.sock',
        network_mode='host',
        tty=True,
        xcom_all=False,
        mount_tmp_dir=False,
        environment=APPLICATION_ARGS
    )
