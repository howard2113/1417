import time
import pandas as pd
import requests
import json
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

'''
捷運進出站人數表(mrt_count)
"TicketType": "一般",
"TrainType": "捷運",
"StationNo": "O1",
"StationName": "西子灣站",
"TranscationDate": "2021-09-13 06:00:00",
"EnterCount": 7,
"ExitCount": 1,
"SrcUpdateTime": "2021-09-13 15:45:00",
"UpdateTime": "2021-09-13 15:45:00",
"InfoTime": "2021-09-13 06:00:00",
"InfoDate": "2021-09-13"
'''

mrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/MrtTransCount?$format=json''', headers=cfg['iis_api_header'])
mrt_str = mrt_res.content.decode('utf-8')
mrt_list = json.loads(mrt_str)
mrt_df = pd.json_normalize(mrt_list)
mrt_df.rename(columns={"TrainType": "train_type", "StationName": "station_name", "EnterCount": "enter", "ExitCount": "exit", "SrcUpdateTime": "src_time", "TranscationDate": "transaction_date"}, inplace=True)

mrt_df["enter_count"] = mrt_df.groupby('station_name')["enter"].transform('sum')
mrt_df["exit_count"] = mrt_df.groupby('station_name')["exit"].transform('sum')
mrt_df.drop_duplicates(subset=['station_name'], keep='last', inplace=True)
mrt_df = mrt_df[['train_type', 'station_name', 'enter', "enter_count", "exit_count", 'exit', 'src_time', 'transaction_date']]
mrt_df['enter_rank'] = 0
mrt_df['exit_rank'] = 0
engine.execute("DELETE FROM mrt_count")
mrt_df.to_sql('mrt_count', engine, if_exists='append', index=False, chunksize=500, )

