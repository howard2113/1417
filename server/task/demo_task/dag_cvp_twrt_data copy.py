import os
import time
import pandas as pd
import requests
import logging
import json
import gspread
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from oauth2client.service_account import ServiceAccountCredentials as SAC


def start():
    cfg = json.load(open(f"{os.environ['PYTHON_PATH_1398']}/config/config.json", 'r'))
    Base = declarative_base()
    engine = create_engine(cfg['db'], echo=True)
    DB_session = sessionmaker(engine)
    db_session = DB_session()
    Base.metadata.create_all(engine)
    now = datetime.now()
    hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

    cvp_twrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpTwrtData?$format=json''', headers=cfg['iis_api_header'])
    print('cvp_twrt_res', cvp_twrt_res)
    cvp_twrt_str = cvp_twrt_res.content.decode('utf-8')
    cvp_twrt_list = json.loads(cvp_twrt_str)
    cvp_twrt_df = pd.json_normalize(cvp_twrt_list)[['Name', 'North', 'South', 'West', 'East', 'NorthEast', 'NorthWest', 'SouthEast', 'SouthWest', 'SrcUpdateTime']]
    cvp_twrt_df.rename(columns={"Name": "name", "North": "north", "South": "south", "West": "west", "East": "east", "NorthEast": "north_east", "NorthWest": "north_west", "SouthEast": "south_east", "SouthWest": "south_west", "SrcUpdateTime": "src_time"}, inplace=True)

    cvp_twrt_df['sum'] = cvp_twrt_df['north'] + cvp_twrt_df['south'] + cvp_twrt_df['west'] + cvp_twrt_df['east'] + cvp_twrt_df['north_east'] + cvp_twrt_df['north_west'] + cvp_twrt_df['south_east'] + cvp_twrt_df['south_west']
    cvp_twrt_df['north_percent'] = cvp_twrt_df['north'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['south_percent'] = cvp_twrt_df['south'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['west_percent'] = cvp_twrt_df['west'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['east_percent'] = cvp_twrt_df['east'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['north_east_percent'] = cvp_twrt_df['north_east'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['north_west_percent'] = cvp_twrt_df['north_west'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['south_east_percent'] = cvp_twrt_df['south_east'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df['south_west_percent'] = cvp_twrt_df['south_west'] / cvp_twrt_df['sum'] * 100
    cvp_twrt_df.drop(['sum'], axis=1, inplace=True)
    engine.execute("DELETE FROM cvp_twrt_data")
    cvp_twrt_df.to_sql('cvp_twrt_data', engine, if_exists='append', index=False, chunksize=500, )



# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'thia',
    'depends_on_past': False,
    # 'start_date': datetime(2021, 8, 20, 16, 54, 0),
    'start_date': datetime.now() - timedelta(minutes=5),
    'email': ['luckyboy1688888@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    # 'end_date': datetime(2020, 2, 29),
    'execution_timeout': timedelta(seconds=60),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
}

#                    m h dom mon dow
# schedule_interval='*/1 * * * *'
dag = DAG(
    dag_id='cvp_twrt_data',
    description='八方位即時資料',
    default_args=default_args,
    schedule_interval='1,6,11,16,21,26,31,36,41,46,51,56 * * * *'
)


cvp_twrt_data_start = PythonOperator(
    task_id='cvp_twrt_data_start',
    python_callable=start,
    provide_context=True,
    dag=dag
)

cvp_twrt_data_start