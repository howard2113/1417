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


def colculate_bus_data(df, id_str, name_str, direction, now_dt):
    if len(df.index) > 0:
        last_row = df.iloc[-1]
        default_data = _default_data.copy()
        default_data['id'] = id_str
        default_data['name'] = name_str
        default_data['direction'] = direction
        default_data['src_time'] = last_row['data_time']
        default_data['update_time'] = now_dt
        default_data['count'] = len(df.index)
        default_data['people'] = df['搭乘人數'].sum()
        default_data['full_rate'] = last_row['搭乘人數'] / 30
        sql_str = sql_insert_if_not_exist('bus_dynamic', default_data, ['id'], {'count': default_data['count'], 'people': default_data['people'], 'full_rate': default_data['full_rate'], 'src_time': default_data['src_time'], 'update_time': now})
        db_session.execute(sql_str)
        db_session.commit()


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
g_sheets = gspread.authorize(Connect)

now = datetime.now()
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)
go_back_divider = now.replace(hour=10, minute=30, second=0, microsecond=0)
bus_total_seat = 30
# =====================================接駁車=====================================
# 凌晨12點歸零所有小時資料
if now.hour == 0 and now.minute <= 30:
    engine.execute(f"DELETE FROM bus_dynamic")
# 旗津線
# 時間戳記  發車時間  搭乘人數
Sheet = g_sheets.open_by_key('1fpzQ0C4RV0nwmgp77nJrZv6WQIJyamrQRB-5KOwYhqQ')
bus_data_list = Sheet.sheet1.get_all_records()
bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_go_data_df = bus_data_df[bus_data_df['data_time'] <= go_back_divider]
    bus_back_data_df = bus_data_df[bus_data_df['data_time'] > go_back_divider]
    colculate_bus_data(bus_go_data_df, 'bus1', '旗津線', 1, now)
    colculate_bus_data(bus_back_data_df, 'bus2', '旗津線', 2, now)

# 高流線
# 時間戳記  發車時間  搭乘人數
Sheet = g_sheets.open_by_key('1gt1q7OX6ymxqIdSWAu-HPHcYLDPx7Qxr99V3rPej-P4')
bus_data_list = Sheet.sheet1.get_all_records()
bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_go_data_df = bus_data_df[bus_data_df['data_time'] <= go_back_divider]
    bus_back_data_df = bus_data_df[bus_data_df['data_time'] > go_back_divider]
    colculate_bus_data(bus_go_data_df, 'bus3', '高流線', 1, now)
    colculate_bus_data(bus_back_data_df, 'bus4', '高流線', 2, now)

# 西子灣線
# 時間戳記  發車時間  搭乘人數
Sheet = g_sheets.open_by_key('10bDkzqrFhkDNrvUVTUiakZ-FOM3OewuPf-UvkJxWOJ4')
bus_data_list = Sheet.sheet1.get_all_records()
bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_go_data_df = bus_data_df[bus_data_df['data_time'] <= go_back_divider]
    bus_back_data_df = bus_data_df[bus_data_df['data_time'] > go_back_divider]
    colculate_bus_data(bus_go_data_df, 'bus5', '西子灣線', 1, now)
    colculate_bus_data(bus_back_data_df, 'bus6', '西子灣線', 2, now)


# 旗鼓航線
# 時間戳記  發車時間  搭乘人數
Sheet = g_sheets.open_by_key('1j8q1IOFmsDPbZmwD04ROVFrhIWVXrGt6kwF0r0axfZQ')
bus_data_list = Sheet.sheet1.get_all_records()
bus_data_df = pd.DataFrame(bus_data_list)
if len(bus_data_df.index) > 0:
    bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
    bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

    bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
    bus_go_data_df = bus_data_df[bus_data_df['data_time'] <= go_back_divider]
    bus_back_data_df = bus_data_df[bus_data_df['data_time'] > go_back_divider]
    colculate_bus_data(bus_go_data_df, 'bus7', '旗鼓航線', 1, now)
    colculate_bus_data(bus_back_data_df, 'bus8', '旗鼓航線', 2, now)

# =====================================機車停車場=====================================

_default_data_moto_parking = {'id': '', 'name': '', 'v_type': 1, 'volumn': '', 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                              'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                              'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

moto_p_map = {'P1河西路': {'id': 'mt1', 'volumn': 1259}, 'P2河東路北': {'id': 'mt2', 'volumn': 1252},
              'P3河東路南': {'id': 'mt3', 'volumn': 990}, 'P4民生一路': {'id': 'mt4', 'volumn': 1590},
              'P5合發立體停車場': {'id': 'mt5', 'volumn': 204}, 'P6海邊路': {'id': 'mt6', 'volumn': 3132},
              'P7林森四路': {'id': 'mt7', 'volumn': 1225}, 'P8成功二路': {'id': 'mt8', 'volumn': 987},
              'P9新光停車場': {'id': 'mt9', 'volumn': 1682}, 'P10夢時代停車場': {'id': 'mt10', 'volumn': 1967}}

# 連線google sheet
sheets = g_sheets.open_by_key('15JuLDaQmkNz0HSv34jZ8hhDX2WWGN7_OLhQE6i4v3ZI')
moto_data_list = sheets.sheet1.get_all_records()
moto_data_df = pd.DataFrame(moto_data_list)

if len(moto_data_df.index) > 0:
    moto_data_df = moto_data_df[moto_data_df['時間戳記'] != '']
    moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('上午', 'AM')
    moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('下午', 'PM')

    moto_data_df['data_time'] = pd.to_datetime(moto_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    moto_data_df = moto_data_df[moto_data_df['data_time'] >= day_start]
    moto_data_df = moto_data_df[moto_data_df['data_time'] <= day_end]
    group_data = moto_data_df.groupby('停車場')
    for name, g_df in group_data:
        last_row = g_df.iloc[-1]
        volumn = moto_p_map[name]['volumn']
        leftspace = volumn - last_row['車輛數']
        default_data = _default_data_moto_parking.copy()
        default_data['id'] = moto_p_map[name]['id']
        default_data['name'] = name
        default_data['volumn'] = volumn
        default_data['leftspace'] = leftspace
        default_data['v_type'] = 2
        default_data[hour_map[last_row['data_time'].hour]] = leftspace
        default_data['src_time'] = last_row['data_time']
        sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], {hour_map[last_row['data_time'].hour]: leftspace, 'src_time': last_row['data_time'], 'update_time': now})
        db_session.execute(sql_str)
    db_session.commit()

# =====================================汽車停車場=====================================

_default_data_car_parking = {'id': '', 'name': '', 'v_type': 1, 'volumn': '', 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                              'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                              'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

moto_p_map = {'衛武營國家藝術文化中心地下停車場': {'id': 'car1', 'volumn': 716}, '文化中心停車場': {'id': 'AD04', 'volumn': 830},
              '前金立體停車場': {'id': 'car3', 'volumn': 648}, '草衙道地下停車場': {'id': 'car4', 'volumn': 967},
              '高雄國際機場停車場': {'id': 'car5', 'volumn': 1051}, '高雄捷運R22青埔站轉乘停車場': {'id': 'car6', 'volumn': 97},
              '捷運都會公園站轉乘停車場': {'id': '448a', 'volumn': 287}, '美術館立體停車場': {'id': 'AA23', 'volumn': 333},
              '國泰青年停車場': {'id': '816', 'volumn': 514}, '捷運大寮站轉乘停車場': {'id': 'car10', 'volumn': 88}}

# 連線google sheet
sheets = g_sheets.open_by_key('1RHZnUfEv7vWf9cGfukFYuqfZhbaUE0lg-KWN-KjfGcQ')
moto_data_list = sheets.sheet1.get_all_records()
moto_data_df = pd.DataFrame(moto_data_list)

if len(moto_data_df.index) > 0:
    moto_data_df = moto_data_df[moto_data_df['時間戳記'] != '']
    moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('上午', 'AM')
    moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('下午', 'PM')

    moto_data_df['data_time'] = pd.to_datetime(moto_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
    moto_data_df = moto_data_df[moto_data_df['data_time'] >= day_start]
    moto_data_df = moto_data_df[moto_data_df['data_time'] <= day_end]
    group_data = moto_data_df.groupby('停車場')
    for name, g_df in group_data:
        last_row = g_df.iloc[-1]
        volumn = moto_p_map[name]['volumn']
        leftspace = volumn - last_row['車輛數']
        default_data = _default_data_moto_parking.copy()
        default_data['id'] = moto_p_map[name]['id']
        default_data['name'] = name
        default_data['volumn'] = volumn
        default_data['leftspace'] = leftspace
        default_data['v_type'] = 1
        default_data[hour_map[last_row['data_time'].hour]] = leftspace
        default_data['src_time'] = last_row['data_time']
        update_dict = {hour_map[last_row['data_time'].hour]: leftspace, 'src_time': last_row['data_time'], 'update_time': now}
        for idx_hr, col_hr in enumerate(hour_map):
            if idx_hr > now.hour:
                update_dict[col_hr] = -1
        sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
        db_session.execute(sql_str)
    db_session.commit()

# =====================================實聯制人數統計=====================================
# QRCode 實聯制累計人數
# 時間戳記	回報時間	進場人數
# Sheet = g_sheets.open_by_key('1StmFYJYV0VTG4ftO3o9ICRyxrMo_AVzxkGuyEG06P-s')
# realname_data_list = Sheet.sheet1.get_all_records()
# realname_data_df = pd.DataFrame(realname_data_list)
#
# if len(realname_data_df.index) > 0:
#     realname_data_df = realname_data_df[realname_data_df['時間戳記'] != '']
#     realname_data_df['時間戳記'] = realname_data_df['時間戳記'].str.replace('上午', 'AM')
#     realname_data_df['時間戳記'] = realname_data_df['時間戳記'].str.replace('下午', 'PM')
#
#     realname_data_df['data_time'] = pd.to_datetime(realname_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
#     realname_data_df = realname_data_df[realname_data_df['data_time'] >= day_start]
#     realname_data_df = realname_data_df[realname_data_df['data_time'] <= day_end]
#     if len(realname_data_df.index) > 0:
#         realname_count = realname_data_df['進場人數'].sum()
#         sql_str = sql_update('cvp_popu_data', {'name': '2021國慶煙火'}, {'realname_count': realname_count})
#         db_session.execute(sql_str)
#         db_session.commit()

