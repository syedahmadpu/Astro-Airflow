

from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
from datetime import datetime, timedelta
import json

##Define DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=datetime.now() - timedelta(days=1),
    schedule='@daily', # Added a schedule for clarity
    catchup=False
) as dag:

    ## step 1: Create the table if it doesnt exists
    @task
    def create_table():
        ## initialize the Postgreshook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")

        ## SQL Query to create the table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS apod_data(
            id SERIAL PRIMARY KEY,
            title VARCHAR(255),
            explanation TEXT,
            url TEXT,
            date DATE,
            media_type VARCHAR(50)
        );
        """
        # CORRECTED: This line is now correctly indented to be inside the function
        postgres_hook.run(create_table_query)

    ## Step 2: Extract the NASA API Data
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key": "{{conn.nasa_api.extra_dejson.api_key}}"},
        response_filter=lambda response: response.json()
    )

    ## Step 3: Transform the data
    @task
    def transform_apod_data(response):
        apod_data = {
            'title': response.get('title', ''),
            'explanation': response.get('explanation', ''),
            'url': response.get('url', ''),
            'date': response.get('date', ''),
            'media_type': response.get('media_type', '')
        }
        return apod_data

    ## Step 4: Load the data into Postgres SQL
    @task
    def load_data_to_postgres(apod_data): # CORRECTED: Changed parameter name for consistency
        ## initialize the PostgresHook
        postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
        ## define the SQL Insert Query
        insert_query = """
        INSERT INTO apod_data(title, explanation, url, date, media_type)
        VALUES (%s, %s, %s, %s, %s);
        """
        ### Execute the SQL Query
        postgres_hook.run(
            insert_query,
            parameters=(
                apod_data['title'],
                apod_data['explanation'],
                apod_data['url'],
                apod_data['date'],
                apod_data['media_type']
              ) 
         )
        

    ## Step5: Verify the data DBViewer # to validate data entering into postgres or not?






    ## Step 6: Set Dependency
    ## Extract
    create_table() >> extract_apod ## Ensure the table is create before extraction
    api_response = extract_apod.output ## the.output  atrbuteis a bridge that allows a traditional Airflow operator (like SimpleHttpOperator) to pass its result to a modern TaskFlow API task (one decorated with @task).
    ## Transform
    transformed_data = transform_apod_data(api_response)
    ## Load
    load_data_to_postgres(transformed_data)