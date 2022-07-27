import time
import pandas as pd
import requests
import json
import glob
import random
from util.database import mysql2csv
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from util.sql_build import sql_insert_if_not_exist

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

'''
捷運進出站人數表(mrt_count)
 {
    "ApiID": "21",
    "Status": "1",
    "Msg": "驗證成功",
    "Name": "2021國慶煙火",
    "Lat": 22.61342912,
    "Lon": 120.2921535,
    "Gid": "101061001",
    "Population": 3,
    "DataTime": "2021-09-13 16:20:00",
    "SrcUpdateTime": "2021-09-13 16:20:00",
    "UpdateTime": "2021-09-13 16:40:00",
    "InfoTime": "2021-09-13 16:20:00",
    "InfoDate": "2021-09-13"
  },
  
  gid
population
lat
lon
src_time
update_time
'''

new_cvp_rt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpRtData?$format=json''', headers=cfg['iis_api_header'])
new_cvp_rt_str = new_cvp_rt_res.content.decode('utf-8')
new_cvp_rt_list = json.loads(new_cvp_rt_str)
new_cvp_rt_df = pd.json_normalize(new_cvp_rt_list)[['Gid', 'Population', 'Lat', 'Lon', 'SrcUpdateTime']]
new_cvp_rt_df.rename(columns={"Gid": "gid", "Population": "population", "Lat": "lat", "Lon": "lon", "SrcUpdateTime": "src_time"}, inplace=True)

# 凌晨清空
now = datetime.now()
if now.hour == 0 and now.minute <= 5:
    engine.execute("DELETE FROM cvp_rt_grid_data")

# 更新人潮網格資料
for idx, new_cvp_rt_data in new_cvp_rt_df.iterrows():
    default_data = {'gid': new_cvp_rt_data['gid'], 'population': new_cvp_rt_data['population'], 'lat': new_cvp_rt_data['lat'], 'lon': new_cvp_rt_data['lon'], 'src_time': new_cvp_rt_data['src_time']}
    update_dict = {'population': new_cvp_rt_data['population'], 'src_time': new_cvp_rt_data['src_time']}
    sql_str = sql_insert_if_not_exist('cvp_rt_grid_data', default_data, ['gid', 'src_time'], update_dict)
    db_session.execute(sql_str)

# 更新人潮區域統計資料
sub_grid_area_df = pd.read_sql(f"SELECT * FROM sub_grid_area", con=engine)
merge_df = pd.merge(new_cvp_rt_df, sub_grid_area_df, on='gid', how='left')
group_data = merge_df.groupby('name')

for name, g_df in group_data:
    last_row = g_df.iloc[-1]
    default_data = {'name': name, 'count': g_df['population'].sum(), 'src_time': last_row['src_time']}
    sql_str = sql_insert_if_not_exist('sub_grid_count', default_data, ['name'], {'count': g_df['population'].sum(), 'src_time': last_row['src_time']})
    db_session.execute(sql_str)

db_session.commit()
