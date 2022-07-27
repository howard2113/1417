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
from oauth2client.service_account import ServiceAccountCredentials as SAC
from utils.sql_build import sql_insert_if_not_exist, sql_insert

# 設定資料庫
cfg = json.load(open(f"config/config.json", 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
now = datetime.now()
now = datetime.strptime('2021-10-10 23:59:59', '%Y-%m-%d %H:%M:%S')
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)

api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

_default_data = {'id': '', 'name': '', 'v_type': 1, 'volumn': '', 'leftspace': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                 'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                 'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

black_parking = ['停4679', 'AD04', '停4370', '停4026', '停3364', '448a', 'AA23', '816']


def start():
    if now.hour == 0 and now.minute <= 5:
        engine.execute("DELETE FROM parking_outer_left_space_dynamic")

    static_df = pd.read_sql(f"SELECT id, name, v_type, volumn FROM parking_outer_static", con=engine)

    # availability_res = requests.get(f'''{cfg['iis_api_url']}/Parking/api/OffStreet/ParkingAvailability/Provider/TBKC?$format=json''', headers=api_headers)
    # print('availability_res', availability_res)
    # availability_str = availability_res.content.decode('utf-8')
    # availability_list = json.loads(availability_str)
    # api_p_dynamic_df = pd.DataFrame(availability_list)[['ID', 'LeftSpace', 'SrcUpdateTime']]
    # id    Name               Volumn    LeftSpace   x1       x2     x3   SrcUpdateTime        x4                  x5                  x6                  x7
    # 093	三鳳中街機車		136	      未提供	   1	  null	   1	2021-10-10 00:58:33	2021-10-10 00:58:33	2021-10-10 00:58:00	2021-10-10 00:58:33	2021-10-10
    header = ['ID', 'Name', 'x0', 'Volumn', 'LeftSpace', 'x1', 'x2', 'x3', 'SrcUpdateTime', 'x4', 'x5', 'x6', 'x7']
    api_p_dynamic_df = pd.read_csv(r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\car_park_tbkc_hour_availability_202110140942.csv")[['id', 'total_volumn', 'total_left_space', 'SrcUpdateTime']]
    # [['ID', 'Volumn', 'LeftSpace', 'SrcUpdateTime']]
    api_p_dynamic_df.fillna(-1, inplace=True)
    api_p_dynamic_df.replace('未提供', -1, inplace=True)
    api_p_dynamic_df.rename(columns={"ID": "id", 'total_volumn': 'volumn', "total_left_space": "leftspace", "SrcUpdateTime": "src_time"}, inplace=True)
    api_p_dynamic_df = pd.merge(api_p_dynamic_df, static_df, on='id', how='inner')

    for idx, api_park_data in api_p_dynamic_df.iterrows():
        if api_park_data['id'] not in black_parking:
            default_data = _default_data.copy()
            default_data['id'] = api_park_data['id']
            default_data['name'] = api_park_data['name']
            default_data['volumn'] = api_park_data['volumn_x']
            default_data['leftspace'] = api_park_data['leftspace']
            default_data['src_time'] = api_park_data['src_time']
            src_datetime = datetime.strptime(api_park_data['src_time'], '%Y-%m-%d %H:%M:%S.%f')
            default_data[hour_map[src_datetime.hour]] = api_park_data['leftspace']
            update_dict = {hour_map[src_datetime.hour]: api_park_data['leftspace'], 'volumn': api_park_data['volumn_x'], 'leftspace': api_park_data['leftspace'], 'src_time': api_park_data['src_time'], 'update_time': now}
            # sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
            # db_session.execute(sql_str)
            sql_str = sql_insert_if_not_exist('parking_outer_static', {'id': api_park_data['id'], 'volumn': api_park_data['volumn_x']}, ['id'], {'volumn': api_park_data['volumn_x']})
            db_session.execute(sql_str)

    db_session.commit()


start()
