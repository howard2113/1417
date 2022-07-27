import os
import time
import pandas as pd
import requests
import logging
import json
import gspread
from datetime import datetime, timedelta
from utils.sql_build import sql_insert_if_not_exist, sql_update
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from oauth2client.service_account import ServiceAccountCredentials as SAC

def colculate_bus_data(df, id_str, name_str, direction, now_dt):
    if len(df.index) > 0:
        default_data = {'id': '', 'name': '', 'direction': '', 'count': 0, 'people': 0, 'full_rate': 0, 'src_time': '', 'update_time': ''}
        last_row = df.iloc[-1]
        default_data['id'] = id_str
        default_data['name'] = name_str
        default_data['direction'] = direction
        default_data['src_time'] = last_row['data_time']
        default_data['update_time'] = now_dt
        default_data['count'] = df['載客趟次'].sum()
        default_data['people'] = df['搭乘人數'].sum()
        default_data['full_rate'] = last_row['搭乘人數'] / 30
        sql_str = sql_insert_if_not_exist('bus_dynamic', default_data, ['id'], {'count': default_data['count'], 'people': default_data['people'], 'full_rate': default_data['full_rate'], 'src_time': default_data['src_time'], 'update_time': now})
        db_session.execute(sql_str)
        db_session.commit()

# 設定資料庫
cfg = json.load(open(f"{os.environ['PYTHON_PATH_1398']}/config/config.json", 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
now = datetime.now()
now = datetime.strptime('2021-10-10 00:00:00', '%Y-%m-%d %H:%M:%S')
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)
go_back_divider = now.replace(hour=10, minute=30, second=0, microsecond=0)
bus_total_seat = 30

# 設定google api
google_key_json = f"{os.environ['PYTHON_PATH_1398']}/config/alpine-sentry-325407-58063405de05.json"  # Json 的單引號內容請改成個人下載的金鑰
google_sheet_url = ['https://spreadsheets.google.com/feeds']
g_connect = SAC.from_json_keyfile_name(google_key_json, google_sheet_url)
g_sheets = gspread.authorize(g_connect)
api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

# 旗津線 google sheet key
g_sheet_key1 = '1xQ1-f_CmtQWVJjsAvEmUBa74DbUWTj_9K_YgoKpDSIE'
# 高流線
g_sheet_key2 = '1Sx6JDWJ2ba0aTtCMjsMOmuMzKLPkIH5Pz-doCBMXADw'
# 台鐵鼓山線
g_sheet_key3 = '1_ukGH_RBFZB1QICQ5Dya_ybQpuGm8I1B2SgBTFf2ulc'
# 旗鼓航線
g_sheet_key4 = '1OCNneFSi0OHi_jrWOGPfqUFVhNS3CaAB69B_9YlAeng'
# 機車停車場
g_sheet_key5 = '15JuLDaQmkNz0HSv34jZ8hhDX2WWGN7_OLhQE6i4v3ZI'
# 汽車停車場
g_sheet_key6 = '1RHZnUfEv7vWf9cGfukFYuqfZhbaUE0lg-KWN-KjfGcQ'


def start():
    # =====================================接駁車=====================================
    # 凌晨12點歸零所有小時資料
    if now.hour == 0 and now.minute <= 30:
        engine.execute(f"DELETE FROM bus_dynamic")
    # 旗津線 bus1 bus2
    # 時間戳記	接駁車方向	載客趟次	發車時間	搭乘人數
    Sheet = g_sheets.open_by_key(g_sheet_key1)
    bus_data_list = Sheet.sheet1.get_all_records()
    bus_data_df = pd.DataFrame(bus_data_list)
    if len(bus_data_df.index) > 0:
        bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

        bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
        bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
        bus_data_df = bus_data_df[bus_data_df['data_time'] < day_end]
        bus_go_data_df = bus_data_df[bus_data_df['接駁車方向'] == '往']
        bus_back_data_df = bus_data_df[bus_data_df['接駁車方向'] == '返']
        colculate_bus_data(bus_go_data_df, 'bus1', '旗津線', 1, now)
        colculate_bus_data(bus_back_data_df, 'bus2', '旗津線', 2, now)

    # 高流線 bus3 bus4
    # 時間戳記	接駁車方向	載客趟次	發車時間	搭乘人數
    Sheet = g_sheets.open_by_key(g_sheet_key2)
    bus_data_list = Sheet.sheet1.get_all_records()
    bus_data_df = pd.DataFrame(bus_data_list)
    if len(bus_data_df.index) > 0:
        bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

        bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
        bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
        bus_data_df = bus_data_df[bus_data_df['data_time'] < day_end]
        bus_go_data_df = bus_data_df[bus_data_df['接駁車方向'] == '往']
        bus_back_data_df = bus_data_df[bus_data_df['接駁車方向'] == '返']
        colculate_bus_data(bus_go_data_df, 'bus3', '高流線', 1, now)
        colculate_bus_data(bus_back_data_df, 'bus4', '高流線', 2, now)

    # 台鐵鼓山線  bus5 bus6
    # 時間戳記	接駁車方向	載客趟次	發車時間	搭乘人數
    Sheet = g_sheets.open_by_key(g_sheet_key3)
    bus_data_list = Sheet.sheet1.get_all_records()
    bus_data_df = pd.DataFrame(bus_data_list)
    if len(bus_data_df.index) > 0:
        bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

        bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
        bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
        bus_data_df = bus_data_df[bus_data_df['data_time'] < day_end]
        bus_go_data_df = bus_data_df[bus_data_df['接駁車方向'] == '往']
        bus_back_data_df = bus_data_df[bus_data_df['接駁車方向'] == '返']
        colculate_bus_data(bus_go_data_df, 'bus5', '台鐵鼓山線', 1, now)
        colculate_bus_data(bus_back_data_df, 'bus6', '台鐵鼓山線', 2, now)


    # 旗鼓航線  bus7 bus8
    # 時間戳記	接駁車方向	載客趟次	發車時間	搭乘人數
    Sheet = g_sheets.open_by_key(g_sheet_key4)
    bus_data_list = Sheet.sheet1.get_all_records()
    bus_data_df = pd.DataFrame(bus_data_list)
    if len(bus_data_df.index) > 0:
        bus_data_df = bus_data_df[bus_data_df['時間戳記'] != '']
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('上午', 'AM')
        bus_data_df['時間戳記'] = bus_data_df['時間戳記'].str.replace('下午', 'PM')

        bus_data_df['data_time'] = pd.to_datetime(bus_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
        bus_data_df = bus_data_df[bus_data_df['data_time'] >= day_start]
        bus_data_df = bus_data_df[bus_data_df['data_time'] < day_end]
        bus_go_data_df = bus_data_df[bus_data_df['接駁車方向'] == '旗津(往)']
        bus_back_data_df = bus_data_df[bus_data_df['接駁車方向'] == '鼓山(返)']
        colculate_bus_data(bus_go_data_df, 'bus7', '旗鼓航線', 1, now)
        colculate_bus_data(bus_back_data_df, 'bus8', '旗鼓航線', 2, now)

    # =====================================機車停車場=====================================

    _default_data_moto_parking = {'id': '', 'name': '', 'v_type': 2, 'volumn': '', 'leftspace': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                                'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                                'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

    moto_p_map = {'P1河西路': {'id': 'mt1', 'volumn': 1259}, 'P2河東路北': {'id': 'mt2', 'volumn': 1252},
                'P3河東路南': {'id': 'mt3', 'volumn': 990}, 'P4民生一路': {'id': 'mt4', 'volumn': 1590},
                'P5合發立體停車場': {'id': 'mt5', 'volumn': 204}, 'P6海邊路': {'id': 'mt6', 'volumn': 3132},
                'P7林森四路': {'id': 'mt7', 'volumn': 1225}, 'P8成功二路': {'id': 'mt8', 'volumn': 987},
                'P9新光停車場': {'id': 'mt9', 'volumn': 1682}, 'P10夢時代停車場': {'id': 'mt10', 'volumn': 1967}}

    for k, moto_p in moto_p_map.items():
        default_data = _default_data_moto_parking.copy()
        default_data['id'] = moto_p['id']
        default_data['name'] = k
        default_data['volumn'] = moto_p['volumn']
        default_data['src_time'] = now
        update_dict = {'volumn':moto_p['volumn'], 'src_time': now}
        sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
        db_session.execute(sql_str)


    sheets = g_sheets.open_by_key(g_sheet_key5)
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
            #default_data[hour_map[last_row['data_time'].hour]] = leftspace
            default_data['src_time'] = last_row['data_time']
            update_dict = {hour_map[last_row['data_time'].hour]: leftspace, 'leftspace': leftspace, 'src_time': last_row['data_time'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
            db_session.execute(sql_str)
            for idx, row in  g_df.iterrows():
                leftspace = volumn - row['車輛數']
                sql_str = sql_update('parking_outer_left_space_dynamic', {'id': moto_p_map[name]['id']}, {f"{hour_map[row['data_time'].hour]}": leftspace})
                db_session.execute(sql_str)
        db_session.commit()

    # =====================================汽車停車場=====================================

    _default_data_car_parking = {'id': '', 'name': '', 'v_type': 1, 'volumn': '', 'leftspace': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                                'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                                'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

    car_p_map = {'衛武營國家藝術文化中心地下停車場': {'id': '停4679', 'volumn': 716}, '文化中心停車場': {'id': 'AD04', 'volumn': 830},
                '前金立體停車場': {'id': '停4370', 'volumn': 648}, '草衙道地下停車場': {'id': '停4026', 'volumn': 967},
                '高雄國際機場停車場': {'id': 'car5', 'volumn': 1051}, '高雄捷運R22青埔站轉乘停車場': {'id': '停3364', 'volumn': 97},
                '捷運都會公園站轉乘停車場': {'id': '448a', 'volumn': 287}, '美術館立體停車場': {'id': 'AA23', 'volumn': 333},
                '國泰青年停車場': {'id': '816', 'volumn': 514}, '捷運大寮站轉乘停車場': {'id': 'car10', 'volumn': 88}}


    for k, car_p in car_p_map.items():
        default_data = _default_data_car_parking.copy()
        default_data['id'] = car_p['id']
        default_data['name'] = k
        default_data['volumn'] = car_p['volumn']
        default_data['src_time'] = now
        update_dict = {'volumn':car_p['volumn'], 'src_time': now}
        sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
        db_session.execute(sql_str)

    sheets = g_sheets.open_by_key(g_sheet_key6)
    car_data_list = sheets.sheet1.get_all_records()
    car_data_df = pd.DataFrame(car_data_list)

    if len(car_data_df.index) > 0:
        car_data_df = car_data_df[car_data_df['時間戳記'] != '']
        car_data_df['時間戳記'] = car_data_df['時間戳記'].str.replace('上午', 'AM')
        car_data_df['時間戳記'] = car_data_df['時間戳記'].str.replace('下午', 'PM')

        car_data_df['data_time'] = pd.to_datetime(car_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')
        car_data_df = car_data_df[car_data_df['data_time'] >= day_start]
        car_data_df = car_data_df[car_data_df['data_time'] <= day_end]
        group_data = car_data_df.groupby('停車場')
        for name, g_df in group_data:
            last_row = g_df.iloc[-1]
            volumn = car_p_map[name]['volumn']
            leftspace = volumn - last_row['車輛數']
            default_data = _default_data_car_parking.copy()
            default_data['id'] = car_p_map[name]['id']
            default_data['name'] = name
            default_data['volumn'] = volumn
            #default_data['leftspace'] = leftspace
            default_data['v_type'] = 1
            default_data[hour_map[last_row['data_time'].hour]] = leftspace
            default_data['src_time'] = last_row['data_time']
            update_dict = {hour_map[last_row['data_time'].hour]: leftspace, 'leftspace': leftspace, 'src_time': last_row['data_time'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('parking_outer_left_space_dynamic', default_data, ['id'], update_dict)
            db_session.execute(sql_str)
            for idx, row in  g_df.iterrows():
                leftspace = volumn - row['車輛數']
                sql_str = sql_update('parking_outer_left_space_dynamic', {'id': car_p_map[name]['id']}, {f"{hour_map[row['data_time'].hour]}": leftspace})
                db_session.execute(sql_str)
        db_session.commit()



# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'thia',
    'depends_on_past': False,
    'start_date': datetime.now() - timedelta(minutes=5),
    'email': ['luckyboy1688888@gmail.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'execution_timeout': timedelta(seconds=30),
}

#                    m h dom mon dow
# schedule_interval='*/1 * * * *'
dag = DAG(
    dag_id='google_form_data',
    description='接駁車&路邊停車場',
    default_args=default_args,
    schedule_interval='*/1 * * * *'
)


google_form_data_start = PythonOperator(
    task_id='google_form_data_start',
    python_callable=start,
    provide_context=True,
    dag=dag
)

google_form_data_start