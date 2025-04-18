from airflow.models import DAG
from airflow.utils.dates import days_ago
from airflow.operators.empty import EmptyOperator
from airflow.operators.bash_operator import BashOperator

with DAG(
    
    'first_dag',
    start_date=days_ago(2),
    schedule_interval='@daily'
    
) as dag:
    
    task_1 = EmptyOperator(task_id='task_1')
    task_2 = EmptyOperator(task_id='task_2')
    task_3 = EmptyOperator(task_id='task_3')
    task_4 = BashOperator(
        
        task_id='make_dir',
        bash_command = 'mkdir -p "/home/steps/Documents/Courses/data-engineering/airflow-alura/airflow-dags/test_directory_{{data_interval_end}}"'
        
        )
    
    task_1 >> [task_2, task_3]
    task_3 >> task_4