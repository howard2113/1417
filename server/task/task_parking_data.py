import time
import numpy as np
import json
import gspread
import requests
import pandas as pd
from datetime import datetime, timedelta
from util.sql_build import sql_insert_if_not_exist, sql_insert
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
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
# 設定google api
google_key_json = 'alpine-sentry-325407-58063405de05.json'  # Json 的單引號內容請改成個人下載的金鑰
google_sheet_url = ['https://spreadsheets.google.com/feeds']
g_connect = SAC.from_json_keyfile_name(google_key_json, google_sheet_url)
g_sheets = gspread.authorize(g_connect)
moto_p_map = {'P1河西路': {'id': 'mt1', 'volumn': 1259}, 'P2河東路北': {'id': 'mt2', 'volumn': 1252},
              'P3河東路南': {'id': 'mt3', 'volumn': 990}, 'P4民生一路': {'id': 'mt4', 'volumn': 1590},
              'P5合發立體停車場': {'id': 'mt5', 'volumn': 204}, 'P6海邊路': {'id': 'mt6', 'volumn': 3132},
              'P7林森四路': {'id': 'mt7', 'volumn': 1225}, 'P8成功二路': {'id': 'mt8', 'volumn': 987},
              'P9新光停車場': {'id': 'mt9', 'volumn': 1682}, 'P10夢時代停車場': {'id': 'mt10', 'volumn': 1967}}
car_p_map = {'衛武營國家藝術文化中心地下停車場': {'id': 'car1', 'volumn': 716}, '文化中心停車場': {'id': 'AD04', 'volumn': 830},
              '前金立體停車場': {'id': 'car3', 'volumn': 648}, '草衙道地下停車場': {'id': 'car4', 'volumn': 967},
              '高雄國際機場停車場': {'id': 'car5', 'volumn': 1051}, '高雄捷運R22青埔站轉乘停車場': {'id': 'car6', 'volumn': 97},
              '捷運都會公園站轉乘停車場': {'id': '448a', 'volumn': 287}, '美術館立體停車場': {'id': 'AA23', 'volumn': 333},
              '國泰青年停車場': {'id': '816', 'volumn': 514}, '捷運大寮站轉乘停車場': {'id': 'car10', 'volumn': 88}}

black_parking = ['AD04', '448a', 'AA23', '816']

api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

_default_data = {'id': '', 'name': '', 'v_type': 1, 'volumn': '', 'leftspace': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

def start():

    static_df = pd.read_sql(f"SELECT id, name, v_type, volumn FROM parking_outer_static", con=engine)

    availability_res = requests.get(f'''{cfg['iis_api_url']}/Parking/api/OffStreet/ParkingAvailability/Provider/TBKC?$format=json''', headers=api_headers)
    availability_str = availability_res.content.decode('utf-8')
    availability_list = json.loads(availability_str)
    api_p_dynamic_df = pd.DataFrame(availability_list)[['ID', 'LeftSpace', 'SrcUpdateTime']]
    api_p_dynamic_df.fillna(-1, inplace=True)
    api_p_dynamic_df.rename(columns={"ID": "id", "Volumn": "volumn", "LeftSpace": "leftspace", "SrcUpdateTime": "src_time"}, inplace=True)
    api_p_dynamic_df = pd.merge(api_p_dynamic_df, static_df, on='id', how='inner')


    for idx, api_park_data in api_p_dynamic_df.iterrows():
        if api_park_data['id'] not in black_parking:
            default_data = _default_data.copy()
            default_data['id'] = api_park_data['id']
            default_data['name'] = api_park_data['name']
            default_data['volumn'] = api_park_data['volumn']
            default_data['src_time'] = api_park_data['src_time']
            default_data['leftspace'] = api_park_data['leftspace']
            src_datetime = datetime.strptime(api_park_data['src_time'], '%Y-%m-%d %H:%M:%S')
            default_data[hour_map[src_datetime.hour]] = api_park_data['leftspace']
            update_dict = {'leftspace': api_park_data['leftspace'], hour_map[src_datetime.hour]: api_park_data['leftspace'], 'src_time': api_park_data['src_time'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)

            db_session.execute(sql_str)

    db_session.commit()


start()
