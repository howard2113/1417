import os.path
import numpy as np
import time
import requests
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float, BigInteger, REAL
from util.database import mysql2csv

from urllib.parse import quote

# src_time = datetime.strptime('2021-07-07 05:00:00 pm'.replace('上午', 'AM').replace('下午', 'PM'), '%Y-%m-%d %H:%M:%S %p')
# src_time = datetime.strptime('2021-07-07 05:00 PM', '%Y-%m-%d %I:%M %p')
# print(src_time)
# from impala.dbapi import connect
# conn = connect(host='220.130.185.37', port=21050, database='default')
# cursor = conn.cursor()
# cursor.execute('SELECT * FROM intercity_bridge_info LIMIT 100')
# print(cursor.description)  # prints the result set's schema
# results = cursor.fetchall()
# print(results)

# tip-r-db-vip
# 192.168.88.23
# Port 3306
# 鼎漢: thi_user/ a?JgVj#8vv

# cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine('postgresql://root:thi168168@127.0.0.1:5432/acer_parking_1393', echo=True)
# engine = create_engine('postgresql://root:thi168168@220.130.185.36:5432/kh_its_1398_v3', echo=True)
# engine = create_engine(f"mysql+pymysql://thi_user:thiits@192.168.88.23:3306/dev_1398", echo=True)
# connection_str = f"mysql+pymysql://thia01:{quote('1qazxcvb@thi')}@210.241.67.133:3306/GoogleTravel"
# engine = create_engine(f"mysql+pymysql://thia01:{quote('1qazxcvb@thi')}@210.241.67.133:3306/GoogleTravel")
# engine = create_engine(f"mysql+pymysql://thia01:thiits@localhost:3306/imageprocess", echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

'''
city
pay_status
update_time
'''

acer_bill = pd.read_csv(r"D:\document\TPE_20211117.csv")[["停車單單號", "格位號碼", "車牌號碼",
                                                          "開單日期", "停車日期時間", "駛離日期時間",
                                                          "停車單時數", "停放分鐘數", "加簽數",
                                                          "停車單金額", "實繳金額", "繳費方式", "計費方式"]]

acer_bill.rename(columns={"停車單單號": "bill_no", "格位號碼": "lac_code", '車牌號碼': 'car_no',
                          "開單日期": "start_date", "停車日期時間": "start_time", "駛離日期時間": "end_time",
                          "停車單時數": "park_hrs", "停放分鐘數": "park_mins", "加簽數": "bill_count",
                          "停車單金額": "amount", "實繳金額": "user_pay", "繳費方式": "pay_type", "計費方式": "fee_type"}, inplace=True)
acer_bill['city'] = "台北"
acer_bill.loc[acer_bill.user_pay > 0, 'pay_status'] = 1
acer_bill.loc[acer_bill.user_pay <= 0, 'pay_status'] = 0

acer_bill.loc[acer_bill.pay_type =='其他', 'pay_type'] = 99
acer_bill.loc[acer_bill.pay_type =='悠遊卡', 'pay_type'] = 3

acer_bill.loc[acer_bill.fee_type =='時段計時', 'fee_type'] = 1
acer_bill.loc[acer_bill.fee_type =='身障計時', 'fee_type'] = 2

acer_bill.to_sql('parking_bills', engine, if_exists='append', index=False, chunksize=500)

print(acer_bill)

# header = ['DeviceID', 'DeliverTime', 'DetectID', 'CarID', 'CarType', 'InTime', 'OutTime', 'CType']
# sub_grid_area = pd.read_csv(r"D:\1338_user_bk\db_bk\mysql-files\CDRawdata.csv", header=None, names=header)
# sub_grid_area.to_sql('CDRawdata', engine, if_exists='append', index=False, chunksize=500)

#
# section_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/Section/AuthorityCode/KHH?$format=json''', headers=cfg['iis_api_header'])
# section_str = section_res.content.decode('utf-8')
# section_list = json.loads(section_str)
# section_df = pd.json_normalize(section_list)
# section_df.to_sql('section_khh', engine, if_exists='replace', index=False, chunksize=500,)

'''
 {
    "SectionID": "L_2001200000000E",
    "SectionName": "高雄都會快速道路(5DRGFH2G到5E13FHBD)",
    "RoadID": "200120",
    "RoadName": "高雄都會快速道路",
    "RoadClass": 2,
    "RoadDirection": "E",
    "RoadSection": {},
    "SectionStart": {
      "PositionLat": 22.6799,
      "PositionLon": 120.29899
    },
    "SectionEnd": {
      "PositionLat": 22.68248,
      "PositionLon": 120.30134
    },
    "UpdateTime": "2021-09-16 12:13:47"
  },
'''

# Base = declarative_base()
# engine = create_engine('impala://220.130.185.37:21050/default', echo=True)
# DB_session = sessionmaker(engine)
# db_session = DB_session()
# Base.metadata.create_all(engine)

# Base = declarative_base()
# engine = create_engine(f"mysql+pymysql://thia01:thiits@localhost:3306/dev_1388", echo=True)
# DB_session = sessionmaker(engine)
# db_session = DB_session()
# Base.metadata.create_all(engine)

# inercity_birdge_weekday_hour = pd.read_csv('1404_fake_data/intercity_onrampdist_day.csv')
# inercity_birdge_weekday_hour['id'] = inercity_birdge_weekday_hour.index
# engine.execute(f"DELETE FROM intercity_onrampdist_day")
# inercity_birdge_weekday_hour.to_sql('intercity_onrampdist_day', engine, if_exists='replace', index=False, chunksize=500, )
# dtype={
#     "lgid": BigInteger,
#
# })

# intercity_bridge_info_df = pd.read_csv('holiday_list_detail.csv')
# intercity_bridge_info_df['id'] = intercity_bridge_info_df.index
# intercity_bridge_info_df.to_sql('holiday_list_detail', engine, if_exists='append', index=False, chunksize=500,)
# dtype={
#     "lgid": BigInteger,
#     "totallanenumber": BigInteger,
#     "detectlanenumber": BigInteger,
#     "device_lng": REAL,
#     "device_lat": REAL,
#     "road_lng": REAL,
#     "road_lat": REAL,
# })

# engine.execute(f"DELETE FROM road_section_vd")
# now = datetime.now()
# intercity_bridge_info_df = pd.read_csv(r"D:\desktop\1398高雄新一代ITS設計與實作計畫\vd_section_v3.csv")[['SectionID', 'RoadName', '方向', '路段起點', '路段終點', '行政區']]
#
# section_res = requests.get(f'''http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/SectionShape/AuthorityCode/KHH?$format=json''', headers={"accept": "*/*", "Authorization": "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"})
# section_str = section_res.content.decode('utf-8')
# section_list = json.loads(section_str)
# section_df = pd.json_normalize(section_list)[['SectionID', 'Geometry']]
# section_df['Geometry'] = section_df['Geometry'].str.replace("LINESTRING", "")
# section_df['Geometry'] = section_df['Geometry'].str.replace('(', '[[')
# section_df['Geometry'] = section_df['Geometry'].str.replace(')', ']]')
# section_df['Geometry'] = section_df['Geometry'].str.replace(',', '],[')
# section_df['Geometry'] = section_df['Geometry'].str.replace(' ', ',')
# merge_df = pd.merge(intercity_bridge_info_df, section_df, on='SectionID', how='left')
#
# merge_df.rename(columns={"SectionID": "id", "RoadName": "name", '行政區': 'area_name', "方向": "direction", "路段起點": "start_pos", "路段終點": "end_pos", 'Geometry': 'geometry'}, inplace=True)
#
# merge_df['src_time'] = now
# merge_df['update_time'] = now
# merge_df.to_sql('road_section_vd', engine, if_exists='append', index=False, chunksize=500)

'''
id,road_id,road_name,station_o,station_d,o_lat,o_lon,d_lat,d_lon,m_lat,m_lon,remark,SrcUpdateTime,UpdateTime,InfoTime,InfoDate
id
name
direction
start_pos
end_pos
geometry
src_time
update_time
'''
# engine.execute(f"DELETE FROM road_section_gvp")
# now = datetime.now()
# gvp_df = pd.read_csv(r"gvp/kao_tomtom_road.csv")[['road_id', 'road_name', 'station_o', 'station_d']]
# gvp_df.rename(columns={"road_id": "SectionID"}, inplace=True)
# section_res = requests.get(f'''http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/GVPSectionShape?$format=json''', headers={"accept": "*/*", "Authorization": "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"})
# section_str = section_res.content.decode('utf-8')
# section_list = json.loads(section_str)
# section_df = pd.json_normalize(section_list)[['SectionID', 'Geometry']]
# section_df['Geometry'] = section_df['Geometry'].str.replace("LINESTRING", "")
# section_df['Geometry'] = section_df['Geometry'].str.replace('(', '')
# section_df['Geometry'] = section_df['Geometry'].str.replace(')', '')
# merge_df = pd.merge(gvp_df, section_df, on='SectionID', how='inner')
#
# merge_df.rename(columns={"SectionID": "id", "road_name": "name", "station_o": "start_pos", "station_d": "end_pos", 'Geometry': 'geometry'}, inplace=True)
# merge_df['direction'] = '暫無'
# merge_df['src_time'] = now
# merge_df['update_time'] = now
# merge_df.to_sql('road_section_gvp', engine, if_exists='append', index=False, chunksize=500)


# start_t = time.time()
# header = ['id', 'name', 'hour', 'speed', 'tti']
# parking_dynamic_df2 = mysql2csv("SELECT * FROM parking_outer_left_space_dynamic", header, engine)
# parking_dynamic_df2.to_pickle()
# print(time.time()-start_t)
# print(time.time()-start_t)

# total_res_df.to_sql('parking_outer_left_space_24h_mean', engine, if_exists='append', index=False, chunksize=500, )


# last_record_time = datetime.strptime('2021-08-08 00:00:00', '%Y-%m-%d %H:%M:%S')  # for test
# dd = last_record_time.weekday()
