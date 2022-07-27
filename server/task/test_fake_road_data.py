import numpy as np
import time
import pandas as pd
import requests
import json
import random
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
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    areaname = db.Column(db.String(10))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
'''
# gvp_road_static_df = pd.read_csv('../csv/kao_tomtom_road.csv')[['road_id', 'road_name', 'o_lat', 'o_lon']]
# gvp_road_static_df = gvp_road_static_df.rename(columns={"road_id": "id", "road_name": "name", "o_lat": "lat", "o_lon": "lon"})
# gvp_road_static_df['areaname'] = ''
# gvp_road_static_df.to_sql('road_static_gvp', engine, if_exists='replace', index=False, chunksize=500, )
# # print(gvp_road_static_df)

# vd_road_static_df = pd.read_csv('../csv/r_vd_history.csv', index_col=0)[['RoadID', 'RoadName', 'PositionLat', 'PositionLon']]
# vd_road_static_df = vd_road_static_df.rename(columns={"RoadID": "id", "RoadName": "name", "PositionLat": "lat", "PositionLon": "lon"})
# vd_road_static_df['areaname'] = ''
# vd_road_static_df = vd_road_static_df.drop_duplicates(subset=['id'], keep='last')
# vd_road_static_df.to_sql('road_static_vd', engine, if_exists='replace', index=False, chunksize=500, )
# print(vd_road_static_df)

#
# # set blank data for test
# total_res_df = pd.DataFrame(columns=['id', 'name', 'speed', 'hour', 'times'])
# for index, row in gvp_road_static_df.iterrows():
#     for hour in range(24):
#         blank_data = {'id': row['id'], 'name': row['name'], 'speed': 0, 'hour': hour, 'times': 0}
#         print(blank_data, 'add ok!')
#         total_res_df = total_res_df.append(blank_data, ignore_index=True)
#
# total_res_df.to_sql('road_speed24h_mean_gvp', engine, if_exists='replace', index=False, chunksize=500, )
#

# # set blank data for test
# total_res_df = pd.DataFrame(columns=['id', 'name', 'speed', 'hour', 'times'])
# for index, row in vd_road_static_df.iterrows():
#     for hour in range(24):
#         blank_data = {'id': row['id'], 'name': row['name'], 'speed': 0, 'hour': hour, 'times': 0}
#         print(blank_data, 'add ok!')
#         total_res_df = total_res_df.append(blank_data, ignore_index=True)
#
# total_res_df.to_sql('road_speed24h_mean_vd', engine, if_exists='replace', index=False, chunksize=500, )


#
# '''
#     "id(路段id)" : "string",
#     "rank(排名)" : "int",
#     "tti(服務績效)" : "float",
#     "speed(時速)" : "float",
# '''
# '''
#     id = db.Column(db.String(10), primary_key=True)
#     name = db.Column(db.String(50))
#     speed = db.Column(db.Integer)
#     hour = db.Column(db.Integer, primary_key=True)
#     times = db.Column(db.Integer)
# '''
#
# mean_gcp_df = pd.read_sql("SELECT * FROM road_speed24h_mean_gvp;", con=engine)
# for day in range(60):
#     road_dynamic_gvp_df = pd.DataFrame(columns=['id', 'rank', 'tti', 'speed'])
#     for hour in range(24):
#         for index, row in gvp_road_static_df.iterrows():
#             _id = row["id"]
#             speed_gvp = random.randrange(20, 50)
#             road_dynamic_gvp_df = road_dynamic_gvp_df.append({'id': row['id'], 'speed': speed_gvp, 'tti': 30}, ignore_index=True)
#
#             mean_gcp_df.loc[(mean_gcp_df["id"] == _id) & (mean_gcp_df["hour"] == hour), 'speed'] += speed_gvp
#             mean_gcp_df.loc[(mean_gcp_df["id"] == _id) & (mean_gcp_df["hour"] == hour), 'times'] += 1
#             print(_id, 'add ok!')
#
#         # road_dynamic_gvp_df['speed'] = road_dynamic_gvp_df['speed'].astype(int)
#         # road_dynamic_gvp_df['rank'] = road_dynamic_gvp_df['speed'].rank(method='first')
#         road_dynamic_gvp_df['rank'] = road_dynamic_gvp_df['speed'].rank()
#         print(road_dynamic_gvp_df)
#         road_dynamic_gvp_df.to_sql('road_dynamic_gvp', engine, if_exists='replace', index=False, chunksize=500, )
#     mean_gcp_df.to_sql('road_speed24h_mean_gvp', engine, if_exists='replace', index=False, chunksize=500, )
#

#
# mean_vd_df = pd.read_sql("SELECT * FROM road_speed24h_mean_vd;", con=engine)
# for day in range(60):
#     road_dynamic_vd_df = pd.DataFrame(columns=['id', 'rank', 'tti', 'speed'])
#     for hour in range(24):
#         for index, row in vd_road_static_df.iterrows():
#             _id = row["id"]
#             speed_vd = random.randrange(20, 50)
#             road_dynamic_vd_df = road_dynamic_vd_df.append({'id': row['id'], 'speed': speed_vd, 'tti': 30}, ignore_index=True)
#
#             mean_vd_df.loc[(mean_vd_df["id"] == _id) & (mean_vd_df["hour"] == hour), 'speed'] += speed_vd
#             mean_vd_df.loc[(mean_vd_df["id"] == _id) & (mean_vd_df["hour"] == hour), 'times'] += 1
#             print('speed_vd', speed_vd, _id, 'add ok!')
#
#         road_dynamic_vd_df['rank'] = road_dynamic_vd_df['speed'].rank()
#         print(road_dynamic_vd_df)
#         road_dynamic_vd_df.to_sql('road_dynamic_vd', engine, if_exists='replace', index=False, chunksize=500, )
#     mean_vd_df.to_sql('road_speed24h_mean_vd', engine, if_exists='replace', index=False, chunksize=500, )
#
#

# VD & GVP set fake data with mean for test
# vd_road_static_df = pd.read_sql("SELECT * FROM road_static_vd;", con=engine)
# road_speed24h_mean_vd_df = pd.read_sql("SELECT * FROM road_speed24h_mean_vd;", con=engine)
#
# gvp_road_static_df = pd.read_sql("SELECT * FROM road_static_gvp;", con=engine)
# road_speed24h_mean_gvp_df = pd.read_sql("SELECT * FROM road_speed24h_mean_gvp;", con=engine)
# last_record_time = datetime.now()
# update_minute_list = [0, 10, 20, 30, 40, 50]
#
# while True:
#     now = datetime.now()
#     print('now:', now)
#     if now.minute in update_minute_list:
#         # VD
#         road_dynamic_vd_df = pd.DataFrame(columns=['id', 'speed', 'tti', 'rank'])
#         for index, row in vd_road_static_df.iterrows():
#             _id = row["id"]
#             speed_vd = random.randrange(20, 50)
#             road_dynamic_vd_df = road_dynamic_vd_df.append({'id': row['id'], 'speed': speed_vd, 'tti': 30}, ignore_index=True)
#
#             road_speed24h_mean_vd_df.loc[(road_speed24h_mean_vd_df["id"] == _id) & (road_speed24h_mean_vd_df["hour"] == now.hour), 'speed'] += speed_vd
#             road_speed24h_mean_vd_df.loc[(road_speed24h_mean_vd_df["id"] == _id) & (road_speed24h_mean_vd_df["hour"] == now.hour), 'times'] += 1
#             print('speed_vd', speed_vd, _id, 'add ok!')
#
#         road_dynamic_vd_df['rank'] = road_dynamic_vd_df['speed'].rank()
#         road_dynamic_vd_df.to_sql('road_dynamic_vd', engine, if_exists='replace', index=False, chunksize=500, )
#         road_speed24h_mean_vd_df.to_sql('road_speed24h_mean_vd', engine, if_exists='replace', index=False, chunksize=500, )
#
#         # GVP
#         gvp_dynamic_df = pd.DataFrame(columns=['id', 'speed', 'tti', 'rank'])
#         for index, row in gvp_road_static_df.iterrows():
#             _id = row["id"]
#             speed_gvp = random.randrange(20, 50)
#             gvp_dynamic_df = gvp_dynamic_df.append({'id': row['id'], 'speed': speed_gvp, 'tti': 30}, ignore_index=True)
#
#             road_speed24h_mean_gvp_df.loc[(road_speed24h_mean_gvp_df["id"] == _id) & (road_speed24h_mean_gvp_df["hour"] == now.hour), 'speed'] += speed_gvp
#             road_speed24h_mean_gvp_df.loc[(road_speed24h_mean_gvp_df["id"] == _id) & (road_speed24h_mean_gvp_df["hour"] == now.hour), 'times'] += 1
#             print('speed_gvp', speed_gvp, _id, 'add ok!')
#
#         gvp_dynamic_df['rank'] = gvp_dynamic_df['speed'].rank()
#         gvp_dynamic_df.to_sql('road_dynamic_gvp', engine, if_exists='replace', index=False, chunksize=500, )
#         road_speed24h_mean_gvp_df.to_sql('road_speed24h_mean_gvp', engine, if_exists='replace', index=False, chunksize=500, )
#
#     time.sleep(60)

#
## VD & GVP set fake dynamic data with mean for test
vd_road_static_df = pd.read_sql("SELECT * FROM road_static_vd;", con=engine)
gvp_road_static_df = pd.read_sql("SELECT * FROM road_static_gvp;", con=engine)
last_record_time = datetime.strptime('2021-08-02 00:00:00', '%Y-%m-%d %H:%M:%S')  # for test
delta_5m_dt = timedelta(minutes=5)
update_minute_list = [0, 10, 20, 30, 40, 50]

road_dynamic_vd_df = pd.DataFrame(columns=['id', 'name', 'hour', 'speed', 'tti'])
gvp_dynamic_df = pd.DataFrame(columns=['id', 'name', 'hour', 'speed', 'tti'])

now = datetime.now()
for index, row in vd_road_static_df.iterrows():
    for hour in range(24):
        if now.hour >= hour:
            speed_vd = random.randrange(20, 50)
            tti_vd = random.randrange(45, 75) / 100
        else:
            speed_vd = -1
        fake_data = {'id': row['id'], 'name': row['name'], 'hour': hour, 'speed': speed_vd, 'tti': tti_vd}
        road_dynamic_vd_df = road_dynamic_vd_df.append(fake_data, ignore_index=True)
engine.execute("DELETE FROM road_dynamic_vd")
road_dynamic_vd_df.to_sql('road_dynamic_vd', engine, if_exists='append', index=False, chunksize=500,
                          dtype={
                                "hour": Integer(),
                                "speed": Integer(),
                                 "tti": Float()
                                 })

for index, row in gvp_road_static_df.iterrows():
    for hour2 in range(24):
        if now.hour >= hour2:
            speed_gvp = random.randrange(20, 50)
            tti_gvp = random.randrange(45, 75) / 100
        else:
            speed_gvp = -1
        fake_data = {'id': row['id'], 'name': row['name'], 'hour': hour2, 'speed': speed_gvp, 'tti': tti_gvp}
        gvp_dynamic_df = gvp_dynamic_df.append(fake_data, ignore_index=True)
engine.execute("DELETE FROM road_dynamic_gvp")
gvp_dynamic_df.to_sql('road_dynamic_gvp', engine, if_exists='append', index=False, chunksize=500,
                      dtype={
                            "hour": Integer(),
                            "speed": Integer(),
                             "tti": Float()
                             })


vd_road_static_df = pd.read_sql("SELECT * FROM road_static_vd;", con=engine)
gvp_road_static_df = pd.read_sql("SELECT * FROM road_static_gvp;", con=engine)

road_dynamic_vd_df = pd.read_sql("SELECT * FROM road_dynamic_vd;", con=engine)
road_dynamic_gvp_df = pd.read_sql("SELECT * FROM road_dynamic_gvp;", con=engine)

last_record_time = datetime.strptime('2021-08-02 00:00:00', '%Y-%m-%d %H:%M:%S')  # for test
delta_5m_dt = timedelta(minutes=5)
update_minute_list = [0, 10, 20, 30, 40, 50]
last_update_minute = -1
while True:
    now = datetime.now()
    print('now:', now)
    # if now.minute in update_minute_list:
    if now.minute in update_minute_list and now.minute != last_update_minute:
        # ==========VD==========
        for index, row in vd_road_static_df.iterrows():
            _id = row["id"]
            speed_vd = random.randrange(20, 50)
            road_dynamic_vd_df.loc[(road_dynamic_vd_df["id"] == _id) & (road_dynamic_vd_df["hour"] == now.hour), 'speed'] = speed_vd
            road_dynamic_vd_df.loc[(road_dynamic_vd_df["id"] == _id) & (road_dynamic_vd_df["hour"] > now.hour), 'speed'] = -1
        engine.execute("DELETE FROM road_dynamic_vd")
        road_dynamic_vd_df.to_sql('road_dynamic_vd', engine, if_exists='append', index=False, chunksize=500, )
        # ==========GVP===========
        for index, row in gvp_road_static_df.iterrows():
            _id = row["id"]
            speed_gvp = random.randrange(20, 50)
            road_dynamic_gvp_df.loc[(road_dynamic_gvp_df["id"] == _id) & (road_dynamic_gvp_df["hour"] == now.hour), 'speed'] = speed_gvp
            road_dynamic_gvp_df.loc[(road_dynamic_gvp_df["id"] == _id) & (road_dynamic_gvp_df["hour"] > now.hour), 'speed'] = -1
        engine.execute("DELETE FROM road_dynamic_gvp")
        road_dynamic_gvp_df.to_sql('road_dynamic_gvp', engine, if_exists='append', index=False, chunksize=500, )

        last_update_minute = now.minute
    time.sleep(10)
