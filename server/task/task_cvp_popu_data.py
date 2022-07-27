import time
import glob
import pandas as pd
import requests
import json
import random
from util.sql_build import sql_insert_if_not_exist, sql_update
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

now = datetime.now()
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

_default_data = {'name': '', 'count': 0, 'h0': 0, 'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'h7': 0, 'h8': 0,
                'h9': 0, 'h10': 0, 'h11': 0, 'h12': 0, 'h13': 0, 'h14': 0, 'h15': 0, 'h16': 0, 'h17': 0, 'h18': 0,
                'h19': 0, 'h20': 0, 'h21': 0, 'h22': 0, 'h23': 0, 'src_time': ''}

'''
即時場內人數
G3 hinet_cvp_twrtdata > population

累積人數統計
E2 hinet_cvp_population50 > allcnt
'''


cvp_popu_df = pd.read_sql(f"SELECT * FROM cvp_popu_data", con=engine)

cvp_twrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpTwrtData?$format=json''', headers=cfg['iis_api_header'])
cvp_twrt_str = cvp_twrt_res.content.decode('utf-8')
cvp_twrt_list = json.loads(cvp_twrt_str)
cvp_twrt_df = pd.json_normalize(cvp_twrt_list)[['Name', 'Population']]
cvp_twrt_df.rename(columns={"Name": "name", "Population": "count"}, inplace=True)

new_cvp_popu_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpPopulation50?$format=json''', headers=cfg['iis_api_header'])
new_cvp_popu_str = new_cvp_popu_res.content.decode('utf-8')
new_cvp_popu_list = json.loads(new_cvp_popu_str)
new_cvp_popu_df = pd.json_normalize(new_cvp_popu_list)[['EvName', 'Allcnt', 'SrcUpdateTime']]
new_cvp_popu_df.rename(columns={"EvName": "name", "Allcnt": "total_count", "SrcUpdateTime": "src_time"}, inplace=True)
new_cvp_popu_df = pd.merge(new_cvp_popu_df, cvp_twrt_df, on='name', how='inner')


for idx, api_cvp_popu_data in new_cvp_popu_df.iterrows():
    default_data = _default_data.copy()
    default_data['name'] = api_cvp_popu_data['name']
    default_data[hour_map[now.hour]] = api_cvp_popu_data['total_count']
    default_data['count'] = api_cvp_popu_data['count']
    default_data['src_time'] = api_cvp_popu_data['src_time']
    src_datetime = datetime.strptime(api_cvp_popu_data['src_time'], '%Y-%m-%d %H:%M:%S')
    update_dict = {hour_map[src_datetime.hour]: api_cvp_popu_data['total_count'], 'count': api_cvp_popu_data['count'], 'src_time': api_cvp_popu_data['src_time'], 'update_time': now}
    for idx_hr, col_hr in enumerate(hour_map):
        if idx_hr > now.hour:
            update_dict[col_hr] = -1
    sql_str = sql_insert_if_not_exist('cvp_popu_data', default_data, ['name'], update_dict)
    db_session.execute(sql_str)



db_session.commit()
