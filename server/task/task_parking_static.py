import time
import json
import pandas as pd
import requests
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

now = datetime.now()

static_res = requests.get(f'''{cfg['iis_api_url']}/Parking/api/OffStreet/CarPark/Provider/TBKC?$format=json''', headers=cfg['iis_api_header'])
static_str = static_res.content.decode('utf-8')
static_list = json.loads(static_str)
static_df = pd.json_normalize(static_list)[['ID', 'AreaName', 'Name', 'Volumn', 'Position.Lat', 'Position.Lng', 'Chargeway', 'SrcUpdateTime']]
static_df.rename(columns={"ID": "id", "AreaName": "areaname", "Name": "name", "Volumn": "volumn", "Position.Lat": "lat", "Position.Lng": "lng", "Chargeway": "fare_description", "SrcUpdateTime": "src_time"}, inplace=True)
static_df['v_type'] = 1
static_df = static_df[static_df['id'] != 'AD04']
static_df = static_df[static_df['id'] != '448a']
static_df = static_df[static_df['id'] != 'AA23']
static_df = static_df[static_df['id'] != '816']

static_df = static_df.append({'id': 'mt1', 'v_type': 2, 'name': 'P1河西路', 'areaname': '國慶臨時機車停車場', 'volumn': 1259, 'lat': 22.627625, 'lng': 120.286863, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt2', 'v_type': 2, 'name': 'P2河東路北', 'areaname': '國慶臨時機車停車場', 'volumn': 1252, 'lat': 22.625201, 'lng': 120.289853, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt3', 'v_type': 2, 'name': 'P3河東路南', 'areaname': '國慶臨時機車停車場', 'volumn': 990, 'lat': 22.622057, 'lng': 120.290841, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt4', 'v_type': 2, 'name': 'P4民生一路', 'areaname': '國慶臨時機車停車場', 'volumn': 1590, 'lat': 22.624079, 'lng': 120.291917, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt5', 'v_type': 2, 'name': 'P5合發立體停車場', 'areaname': '國慶臨時機車停車場', 'volumn': 204, 'lat': 22.627328, 'lng': 120.293096, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt6', 'v_type': 2, 'name': 'P6海邊路', 'areaname': '國慶臨時機車停車場', 'volumn': 3132, 'lat': 22.611393, 'lng': 120.296781, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt7', 'v_type': 2, 'name': 'P7林森四路', 'areaname': '國慶臨時機車停車場', 'volumn': 1225, 'lat': 22.608784, 'lng': 120.301292, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt8', 'v_type': 2, 'name': 'P8成功二路', 'areaname': '國慶臨時機車停車場', 'volumn': 987, 'lat': 22.608356, 'lng': 120.299954, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt9', 'v_type': 2, 'name': 'P9新光停車場', 'areaname': '國慶臨時機車停車場', 'volumn': 1682, 'lat': 22.606359, 'lng': 120.300532, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'mt10', 'v_type': 2, 'name': 'P10夢時代停車場', 'areaname': '國慶臨時機車停車場', 'volumn': 1967, 'lat': 22.596067, 'lng': 120.308581, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)

static_df = static_df.append({'id': 'car1', 'v_type': 1, 'name': '衛武營國家藝術文化中心地下停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 716, 'lat': 22.623630, 'lng': 120.340913, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'AD04', 'v_type': 1, 'name': '文化中心停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 830, 'lat': 22.627123, 'lng': 120.318888, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'car3', 'v_type': 1, 'name': '前金立體停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 648, 'lat': 22.627322, 'lng': 120.293031, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'car4', 'v_type': 1, 'name': '草衙道地下停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 967, 'lat': 22.582795, 'lng': 120.330335, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'car5', 'v_type': 1, 'name': '高雄國際機場停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 1051, 'lat': 22.570486, 'lng': 120.342257, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'car6', 'v_type': 1, 'name': '高雄捷運R22青埔站轉乘停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 97, 'lat': 22.743759, 'lng': 120.317864, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': '448a', 'v_type': 1, 'name': '捷運都會公園站轉乘停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 287, 'lat': 22.73141176, 'lng': 120.32003403, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'AA23', 'v_type': 1, 'name': '美術館立體停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 333, 'lat': 22.6556614, 'lng': 120.285431, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': '816', 'v_type': 1, 'name': '國泰青年停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 514, 'lat': 22.623721, 'lng': 120.348597, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)
static_df = static_df.append({'id': 'car10', 'v_type': 1, 'name': '捷運大寮站轉乘停車場', 'areaname': '國慶汽車轉乘停車場', 'volumn': 88, 'lat': 22.622214, 'lng': 120.392846, 'fare_description': '國慶煙火周邊', 'src_time': now}, ignore_index=True)

engine.execute(f"DELETE FROM parking_outer_static")
static_df.to_sql('parking_outer_static', engine, if_exists='append', index=False, chunksize=500, )
