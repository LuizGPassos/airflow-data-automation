from airflow import DAG
import pendulum
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
import os
import pandas as pd
from dotenv import load_dotenv
from airflow.macros import ds_add

with DAG(
    
    'weather_data',
    start_date=pendulum.datetime(2025, 3, 3, tz="UTC"),
    schedule_interval='0 0 * * 1'
    
) as dag:
    
    task_1 = BashOperator(
        
        task_id='make_dir',
        bash_command = 'mkdir -p "/home/steps/Documents/Courses/data-engineering/airflow-alura/airflow-dags/week_{{data_interval_end.strftime("%Y-%m-%d")}}"'
        
        )
    
    def data_extract(data_interval_end):
        
        load_dotenv()

        API_KEY = os.getenv("API_KEY")
        city = 'Boston'
        URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}/{data_interval_end}/{ds_add(data_interval_end, 7)}?key={API_KEY}&unitGroup=metric&include=days&contentType=csv"

        df = pd.read_csv(URL)

        file_path = f"/home/steps/Documents/Courses/data-engineering/airflow-alura/airflow-dags/week_{data_interval_end}"
        os.makedirs(file_path, exist_ok=True)


        df.to_csv(f"{file_path}/all_weather_data.csv")
        df[['datetime', 'tempmin', 'temp', 'tempmax']].to_csv(f"{file_path}/temp_data.csv")
        df[['datetime', 'description', 'icon']].to_csv(f"{file_path}/info_weather_data.csv")
    
    task_2 = PythonOperator(
        
        task_id = 'data_extract',
        python_callable = data_extract,
        op_kwargs = {"data_interval_end": "{{data_interval_end.strftime('%Y-%m-%d')}}"}
        
    )
    
    task_1 >> task_2
    