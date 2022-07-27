import time
import json
import pandas as pd
import requests
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
last_time_minute = -1
update_minute_list = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

while True:
    now = datetime.now()
    now = now.replace(second=0, microsecond=0)
    print('now:', now)
    # if now.minute in update_minute_list and now.minute != last_time_minute:
    if now.minute in update_minute_list and now.minute != last_time_minute or True:  # for dev
        cps_res = requests.get('https://kpp.tbkc.gov.tw/parking/V1/parking/OffStreet/CarPark/Space')
        cps_xml_str = cps_res.content.decode('utf-8')
        cps_xml_str = cps_xml_str[cps_xml_str.find('<'):]
        cps_static_df = pd.read_xml(cps_xml_str, xpath='//abc:ParkingSpace', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})[['CarParkID', 'TotalSpaces']]

        cp_res = requests.get('https://kpp.tbkc.gov.tw/parking/V1/parking/OffStreet/CarPark')
        cp_xml_str = cp_res.content.decode('utf-8')
        cp_xml_str = cp_xml_str[cp_xml_str.find('<'):]
        cp_static_df = pd.read_xml(cp_xml_str, xpath='//abc:CarPark', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})
        cp_name_df = pd.read_xml(cp_xml_str, xpath='//abc:CarParkName', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})[['Zh_tw']]
        cp_lat_lon_df = pd.read_xml(cp_xml_str, xpath='//abc:CarParkPosition', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})

        cp_static_df = cp_static_df[['CarParkID', 'Description', 'TownName', 'FareDescription']]
        cp_static_df = cp_static_df.join(cp_name_df)
        cp_static_df = cp_static_df.join(cp_lat_lon_df)
        cp_static_df = pd.merge(cp_static_df, cps_static_df, on='CarParkID', how='inner')
        cp_static_df.rename(columns={"CarParkID": "id", "Zh_tw": "name", "TownName": "areaname", "TotalSpaces": "volume", "PositionLat": "lat",
                                     "PositionLon": "lng", "Description": "space_description", "FareDescription": "fare_description"}, inplace=True)
        cp_static_df['update_time'] = now
        cp_static_df['v_type'] = 1

        cp_static_df = cp_static_df.append({'id': 'mt001', 'v_type': 2, 'name': '海邊路(青年二路-苓安路)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt002', 'v_type': 2, 'name': '海邊樂(五福三路-英雄路)2車道', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt003', 'v_type': 2, 'name': '河東路(中正四路-五福三路)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt004', 'v_type': 2, 'name': '中正四路至音樂館間空第)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt005', 'v_type': 2, 'name': '七賢三路(五福四路-公園二路)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt006', 'v_type': 2, 'name': '公園二路(大安街-大勇街)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)
        cp_static_df = cp_static_df.append({'id': 'mt007', 'v_type': 2, 'name': '臨海三路(全段)', 'areaname': '路邊機車', 'volume': 9999, 'lat': 22.6696, 'lng': 120.293, 'space_description': '國慶煙火周邊', 'fare_description': '國慶煙火周邊', 'update_time': now}, ignore_index=True)

        print(cp_static_df)

        engine.execute(f"DELETE FROM parking_outer_static")
        cp_static_df.to_sql('parking_outer_static', engine, if_exists='append', index=False, chunksize=500, )
        last_time_minute = now.minute
    time.sleep(10)
