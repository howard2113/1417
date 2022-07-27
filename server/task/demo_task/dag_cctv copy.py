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
    print(os.getcwd())
    cfg = json.load(open(f"{os.environ['PYTHON_PATH_1398']}/config/config.json", 'r'))
    Base = declarative_base()
    engine = create_engine(cfg['db'], echo=True)
    DB_session = sessionmaker(engine)
    db_session = DB_session()
    Base.metadata.create_all(engine)
    now = datetime.now()
    hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

    api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

    cctv_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/CCTVInKHHList?$format=json''', headers=api_headers)
    cctv_str = cctv_res.content.decode('utf-8')
    cctv_list = json.loads(cctv_str)
    cctv_df = pd.json_normalize(cctv_list)[['CCTVID', 'SurveillanceDescription', 'Position.PositionLon', 'Position.PositionLat', 'VideoStreamURL', 'LayoutMapURL', 'SrcUpdateTime']]
    cctv_df.rename(columns={'CCTVID': 'id', 'SurveillanceDescription': 'name', 'VideoStreamURL': 'url', "Position.PositionLat": "lat", "Position.PositionLon": "lng", "SrcUpdateTime": "src_time", "LayoutMapURL": "img"}, inplace=True)

    engine.execute(f"DELETE FROM cctv_info")
    cctv_df.to_sql('cctv_info', engine, if_exists='append', index=False, chunksize=500, )

start()