from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
import pendulum
import requests
import json

LATITUDE = '51.5074'
LONGITUDE = '-0.1278'
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': pendulum.now().subtract(days=1),
}

## DAG
with DAG(dag_id='weather_etl_pipeline',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:

    @task()
    def extract_weather_data():
        """Extract weather data from Open-Meteo API using Airflow Connection."""
        # Use the HTTP Hook to get data
        # Note: The Base URL (https://api.open-meteo.com) must be defined in the Airflow Connection UI
        http_hook = HttpHook(http_conn_id=API_CONN_ID, method='GET')

        # Build API Endpoint
        # API requires: https://api.open-meteo.com/v1/forecast?latitude=...
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'

        # Request via the HTTP Hook
        response = http_hook.run(endpoint)

        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to fetch weather data: {response.status_code}")

    @task()
    def transform_weather_data(weather_data):
        """Transform the raw data."""
        current_weather = weather_data['current_weather']
        
        # FIXED: Corrected mapping and spelling
        transform_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather['temperature'],      # Fixed spelling
            'windspeed': current_weather['windspeed'],          # Fixed logic
            'winddirection': current_weather['winddirection'],  # Added missing field
            'weathercode': current_weather['weathercode']
        }
        return transform_data

    @task()
    def load_weather_data(transform_data):
        """Load transformed data into Postgres."""
        # FIXED: Typo 'postgress' -> 'postgres'
        pg_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = pg_hook.get_conn()
        cursor = conn.cursor()

        # Create Table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            latitude FLOAT,
            longitude FLOAT,
            temperature FLOAT,
            windspeed FLOAT,
            winddirection FLOAT,
            weathercode INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """)

        # FIXED: Indentation fixed here (moved inside the function)
        cursor.execute("""
        INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            transform_data['latitude'],
            transform_data['longitude'],
            transform_data['temperature'],
            transform_data['windspeed'],
            transform_data['winddirection'],
            transform_data['weathercode']
        ))

        conn.commit()
        cursor.close()

    ## DAG Workflow
    weather_data = extract_weather_data()
    transform_data = transform_weather_data(weather_data)
    load_weather_data(transform_data)