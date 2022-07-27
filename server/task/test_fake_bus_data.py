import time
import pandas as pd
import requests
import json
import random
from datetime import datetime
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
    "id(接駁車路線id)" : "string", 
  "name(接駁車路線名稱)" : "string",
  "count(運載次數)" : "int",
  "people(運載人數)" : "int",

'''
# gvp_road_static_df = pd.read_csv('csv/kao_tomtom_road.csv')[['road_id', 'road_name', 'o_lat', 'o_lon']]
# gvp_road_static_df = gvp_road_static_df.rename(columns={"road_id": "id", "road_name": "name", "o_lat": "lat", "o_lon": "lon"})
# gvp_road_static_df['areaname'] = ''
# # gvp_road_static_df.to_sql('road_static_gvp', engine, if_exists='replace', index=False, chunksize=500, )
# # print(gvp_road_static_df)

# bus_route_df = pd.read_csv('../csv/bus_route_kao.csv', index_col=0)[['route_id', 'route_name_zh']]
# bus_route_df = bus_route_df.rename(columns={"route_id": "id", "route_name_zh": "name"})
# bus_route_df['count'] = 0
# bus_route_df['people'] = 0
# bus_route_df = bus_route_df.drop_duplicates(subset=['id'], keep='last')
# # bus_route_df.to_sql('bus_dynamic', engine, if_exists='replace', index=False, chunksize=500, )
# # print(vd_road_static_df)
#
#
# # set blank data for test
# while True:
#     total_res_df = pd.DataFrame(columns=['id', 'name', 'count', 'people'])
#     for index, row in bus_route_df.iterrows():
#         count = random.randrange(16, 168)
#         people = random.randrange(16, 1688)
#         fake_data = {'id': row['id'], 'name': row['name'], 'count': count, 'people': people}
#         print(fake_data, 'add ok!')
#         total_res_df = total_res_df.append(fake_data, ignore_index=True)
#     total_res_df.to_sql('bus_dynamic', engine, if_exists='replace', index=False, chunksize=500, )
#     time.sleep(60)


bus_dynamic_df = pd.read_sql("SELECT * FROM bus_dynamic;", con=engine)

# set blank data for test

last_record_time = datetime.now()
update_minute_list = [0, 10, 20, 30, 40, 50]

while True:
    now = datetime.now()
    print('now:', now)
    if now.minute in update_minute_list:
        total_res_df = pd.DataFrame(columns=['id', 'name', 'count', 'people'])
        for index, row in bus_dynamic_df.iterrows():
            count = random.randrange(16, 168)
            people = random.randrange(16, 1688)
            fake_data = {'id': row['id'], 'name': row['name'], 'count': count, 'people': people}
            print(fake_data, 'add ok!')
            total_res_df = total_res_df.append(fake_data, ignore_index=True)
        total_res_df.to_sql('bus_dynamic', engine, if_exists='replace', index=False, chunksize=500, )

    time.sleep(10)




header = ['TicketType', 'TrainType', 'StationNo', 'StationName', 'TransactionDate', 'Enter', 'Exit']
# fake_mrt_trans_count_df = mysql2csv('SELECT * FROM mrt_trans_count', header, engine)
fake_mrt_trans_count_df = pd.read_csv('mrt_data/mrt_data.csv')
fake_mrt_trans_count_df['TransactionDate'] = pd.to_datetime(fake_mrt_trans_count_df['TransactionDate'], format='%Y%m%d %H:%M:%S')
fake_mrt_trans_count_df.to_sql(
    'mrt_trans_count',
    engine,
    if_exists='replace',
    index=False,
    chunksize=500,
    dtype={
        "TicketType": Text,
        "TrainType":  Text,
        "StationNo": Text,
        "StationName":  Text,
        "TransactionDate":  DateTime,
        "Enter":  Integer,
        "Exit":  Integer,
    }
)
