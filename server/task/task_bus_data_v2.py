import time
import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from util.sql_build import sql_insert, sql_update, sql_insert_if_not_exist

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
last_time_minute = -1
update_minute_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

_default_data = {'id': '', 'name': '', 'direction': '', 'count': -1, 'people': -1, 'full_rate': -1, 'src_time': '', 'update_time': ''}

Json = 'alpine-sentry-325407-58063405de05.json'  # Json 的單引號內容請改成個人下載的金鑰
Url = ['https://spreadsheets.google.com/feeds']
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

now = datetime.now()
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)
######接駁車
# 時間戳記  發車時間  搭乘人數
Sheet = GoogleSheets.open_by_key('1xSXUEwLWf0VfcxaFPMmLxRszSquuNast2zzB6AIZCYY')
bus_data_list = Sheet.sheet1.get_all_records()

# 凌晨12點歸零所有小時資料
if now.hour == 0 and now.minute <= 30:
    engine.execute(f"DELETE FROM bus_dynamic")

bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_data_df = bus_data_df[bus_data_df['data_time'] <= day_end]
    if len(bus_data_df.index) > 0:
        last_row = bus_data_df.iloc[-1]
        default_data = _default_data.copy()
        default_data['id'] = 'bus1'
        default_data['name'] = '旗津線'
        default_data['direction'] = 1
        if now.hour > 20 and now.minute > 30:
            default_data['direction'] = 2
        default_data['src_time'] = last_row['data_time']
        default_data['update_time'] = now
        default_data['count'] = len(bus_data_df.index)
        default_data['people'] = bus_data_df['搭乘人數'].sum()
        default_data['full_rate'] = last_row['搭乘人數'] / 30
        sql_str = sql_insert_if_not_exist('bus_dynamic', default_data, ['id'], {'count': default_data['count'], 'people': default_data['people'], 'full_rate': default_data['full_rate'], 'src_time': default_data['src_time'], 'update_time': now})
        db_session.execute(sql_str)
        db_session.commit()

Sheet = GoogleSheets.open_by_key('1y-VpUtf5Rm4A2ou_b1qGDgcu88R-Vnl0dMNht2o1vfE')
bus_data_list = Sheet.sheet1.get_all_records()

bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_data_df = bus_data_df[bus_data_df['data_time'] <= day_end]
    if len(bus_data_df.index) > 0:
        last_row = bus_data_df.iloc[-1]
        default_data = _default_data.copy()
        default_data['id'] = 'bus2'
        default_data['name'] = '高流線'
        default_data['direction'] = 1
        if now.hour > 20 and now.minute > 30:
            default_data['direction'] = 2
        default_data['src_time'] = last_row['data_time']
        default_data['update_time'] = now
        default_data['count'] = len(bus_data_df.index)
        default_data['people'] = bus_data_df['搭乘人數'].sum()
        default_data['full_rate'] = last_row['搭乘人數'] / 30
        sql_str = sql_insert_if_not_exist('bus_dynamic', default_data, ['id'], {'count': default_data['count'], 'people': default_data['people'], 'full_rate': default_data['full_rate'], 'src_time': default_data['src_time'], 'update_time': now})
        db_session.execute(sql_str)
        db_session.commit()
