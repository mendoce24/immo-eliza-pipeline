from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.operators.bash import BashOperator
from scraper.id_scraper import id_scraper
from scraper.property_scraper import property_scraper

def mainScraperImmoWeb(**kwargs):
    search_pages_num = 333
    id_scraper(search_pages_num)
    property_scraper(kwargs['ds_nodash'])

with DAG(dag_id="ImmoElizaPipeline", 
        description="Scrapeing information from ImmoWeb.be",
        schedule_interval= "0 0 * * *",
        start_date= datetime(2023, 9, 26), 
        end_date= datetime(2023, 9, 27),
        default_args={"depends_on_past": True}, 
        max_active_runs=1) as dag:
    
    t1= PythonOperator(task_id="ScraperImmoWeb", 
                   python_callable= mainScraperImmoWeb)
    
    t2= FileSensor(task_id= "waiting_file",
                   filepath= "/tmp/properties_data_{{ds_nodash}}.json")
    
    t3= BashOperator(task_id= "TransformCsvFile",
                   bash_command= "echo 'The file has been transform in CSV'")
    
    t4= BashOperator(task_id= "CleanData",
                   bash_command= "echo 'Clean Data'")
    
    t5= BashOperator(task_id= "Modeling",
                   bash_command= "echo 'Modeling'")
    


t1 >> t2 >> t3 >> t4 >> t5