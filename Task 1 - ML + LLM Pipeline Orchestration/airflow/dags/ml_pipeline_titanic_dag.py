from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2023, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    'ml_pipeline_titanic',
    default_args=default_args,
    description='Titanic ML pipeline DAG',
    schedule_interval='@daily',
    catchup=False
) as dag:

    preprocess = BashOperator(
        task_id='preprocess',
        bash_command='python /opt/ml_pipeline/titanic_preprocess.py'
    )

    feature_engineering = BashOperator(
        task_id='feature_engineering',
        bash_command='python /opt/ml_pipeline/titanic_feature_engineering.py'
    )

    train = BashOperator(
        task_id='train',
        bash_command='python /opt/ml_pipeline/titanic_train.py'
    )

    evaluate = BashOperator(
        task_id='evaluate',
        bash_command='python /opt/ml_pipeline/titanic_evaluate.py'
    )

    preprocess >> feature_engineering >> train >> evaluate