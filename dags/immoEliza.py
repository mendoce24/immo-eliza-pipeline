from airflow import DAG
from datetime import datetime
from airflow.operators.python import PythonOperator
from scraper.id_scraper import id_scraper
from scraper.property_scraper import property_scraper

def mainScraperImmoWeb():
    search_pages_num = 333
    id_scraper(search_pages_num)
    property_scraper()

with DAG(dag_id="ImmoElizaPipeline", 
         description="Scrapeing information from ImmoWeb.be",
        schedule_interval= "@once",
        start_date= datetime(2023, 9, 27)) as dag:
    
    t1= PythonOperator(task_id="ScraperImmoWeb", 
                   python_callable= mainScraperImmoWeb)

t1