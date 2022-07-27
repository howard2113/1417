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

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
last_time_minute = -1
update_minute_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

Json = 'alpine-sentry-325407-58063405de05.json'  # Json 的單引號內容請改成個人下載的金鑰
Url = ['https://spreadsheets.google.com/feeds']
Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

p_dynamic_df = pd.read_sql(f"SELECT * FROM parking_outer_left_space_dynamic", con=engine)
# p_24h_mean_df = pd.read_sql(f"SELECT * FROM parking_outer_left_space_24h_mean", con=engine)

moto_p_map = ['海邊路(青年二路-苓安路)', '海邊樂(五福三路-英雄路)2車道', '河東路(中正四路-五福三路)', '中正四路至音樂館間空第)', '七賢三路(五福四路-公園二路)', '公園二路(大安街-大勇街)', '臨海三路(全段)']

while True:
    try:
        now = datetime.now()
        now = now.replace(second=0, microsecond=0)
        print('now:', now)
        # if now.minute in update_minute_list and now.minute != last_time_minute:
        if now.minute in update_minute_list and now.minute != last_time_minute or True:  # for dev
            ######汽車
            res = requests.get('https://kpp.tbkc.gov.tw/parking/V1/parking/OffStreet/CarPark/Availability')
            xml_str = res.content.decode('utf-8')
            xml_str = xml_str[xml_str.find('<'):]
            parking_df = pd.read_xml(xml_str, xpath='//abc:ParkingAvailability', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})
            zh_tw_df = pd.read_xml(xml_str, xpath='//abc:CarParkName', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})
            join_df = parking_df.join(zh_tw_df)
            join_df.drop(['CarParkName', 'Availabilities', 'En', 'ServiceStatus', 'FullStatus', 'ChargeStatus'], axis=1, inplace=True)
            join_df.replace('未提供', -1, inplace=True)
            join_df.replace(np.nan, -1, inplace=True)
            join_df.fillna(-1)
            join_df['AvailableSpaces'] = join_df['AvailableSpaces'].astype('int32')
            join_df.rename(columns={"CarParkID": "id", "Zh_tw": "name", "TotalSpaces": "volume", "DataCollectTime": "src_time"}, inplace=True)
            print(parking_df)

            for idx, api_park_data in join_df.iterrows():
                df_index = p_dynamic_df.index[p_dynamic_df['name'] == api_park_data['name']]
                # 檢查是否存在DB，否則新增一筆
                if len(df_index) <= 0:
                    p_dynamic_df = p_dynamic_df.append({'id': api_park_data['id'], 'v_type': 1, 'name': api_park_data['name'], 'volume': api_park_data['volume'], 'h0': -1, 'h1': -1, 'h2': -1,
                                                        'h3': -1, 'h4': -1, 'h5': -1, 'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                                                        'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': now, 'update_time': now}, ignore_index=True)
                    df_index = p_dynamic_df.index[p_dynamic_df['name'] == api_park_data['name']]

                if now.hour == 0 and now.minute == 0:
                    p_dynamic_df.loc[df_index, hour_map] = -1

                # 過濾 [未提供] 資料
                if api_park_data['AvailableSpaces'] > 0:
                    p_dynamic_df.loc[df_index, hour_map[now.hour]] = api_park_data['AvailableSpaces']
                    # p_24h_mean_df.loc[(p_24h_mean_df['name'] == api_park_data['name']), hour_map[now.hour]] += api_park_data['AvailableSpaces']
                else:
                    p_dynamic_df.loc[df_index, hour_map[now.hour]] = -1

                # p_24h_mean_df.loc[(p_24h_mean_df['name'] == api_park_data['name']), 'collect_count'] += 1
                p_dynamic_df.loc[df_index, 'src_time'] = api_park_data['src_time']
                # p_24h_mean_df.loc[(p_24h_mean_df['name'] == api_park_data['name']), 'src_time'] = api_park_data['src_time']
                print(api_park_data)

            ######機車
            Sheet = GoogleSheets.open_by_key('1sK5DndzfpR1FV1yx-jQmbhr8riYMYRX9HOrr8jLOkbk')
            moto_data_list = Sheet.sheet1.get_all_records()
            moto_data_df = pd.DataFrame(moto_data_list)
            moto_data_df.drop_duplicates(subset=['停車場'], keep='last', inplace=True)

            for idx, moto_data in moto_data_df.iterrows():
                if moto_data['停車場'] in moto_p_map:

                    id_n = moto_p_map.index(moto_data['停車場'])
                    src_time = datetime.strptime(moto_data['時間戳記'].replace('上午', 'AM').replace('下午', 'PM'), '%Y/%m/%d %p %I:%M:%S')

                    df_index = p_dynamic_df.index[p_dynamic_df['name'] == moto_data['停車場']]

                    if id_n >= 0 and len(df_index) <= 0:
                        p_dynamic_df = p_dynamic_df.append({'id': f'mt{id_n + 1}', 'v_type': 2, 'name': moto_data['停車場'], 'volume': 1000, 'h0': -1, 'h1': -1, 'h2': -1,
                                                            'h3': -1, 'h4': -1, 'h5': -1, 'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                                                            'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': src_time, 'update_time': now}, ignore_index=True)
                    # 凌晨12點歸零所有小時資料
                    if now.hour == 0 and now.minute == 0:
                        p_dynamic_df.loc[df_index, hour_map] = -1
                    # 更新單一小時資料
                    if now.hour == src_time.hour:
                        p_dynamic_df.loc[df_index, hour_map[now.hour]] = 1000 - moto_data['車輛數']
                        p_dynamic_df.loc[df_index, 'src_time'] = src_time

            engine.execute(f"DELETE FROM parking_outer_left_space_dynamic")
            # engine.execute(f"DELETE FROM parking_outer_left_space_24h_mean")
            p_dynamic_df.to_sql('parking_outer_left_space_dynamic', engine, if_exists='append', index=False, chunksize=500, )
            # p_24h_mean_df.to_sql('parking_outer_left_space_24h_mean', engine, if_exists='append', index=False, chunksize=500, )
            last_time_minute = now.minute
    except Exception as e:
        int('a')
        print('socket error2:', str(e))

    time.sleep(10)
