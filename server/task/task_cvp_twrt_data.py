import time
import pandas as pd
import requests
import json
import random
from util.database import mysql2csv
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)


cvp_twrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpTwrtData?$format=json''', headers=cfg['iis_api_header'])
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



