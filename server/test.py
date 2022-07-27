import pandas as pd
import requests
import json
from datetime import datetime
import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float

now = datetime.now()

hour_list = pd.date_range(now.strftime('%Y-%m-%d'), periods=24, freq='1H')
for hour, dt in enumerate(hour_list):

    if hour_list[hour-1] <= now < dt:
        print(hour)


# [{
#   "name(停車場名稱)" : "string",
#   "areaname(行政區域)" : "string",
#   "volumn(總格位)" : "int",
#   "lat(緯度)" : "float/decimal",
#   "lng(經度)" : "float/decimal",
# }]

parking_static_url = "https://ptps.tbkc.gov.tw/api/GetAllLot"
post_data = '{"ApiKey":"db0a7b8e9125627853633366a1a50ae78b73315b433f8e17fb02f18d017cbdef"}'
res = requests.post(parking_static_url, json=post_data, headers={"Content-Type": "application/json"})
data = json.loads(res.text)
# parking_static_df = pd.read_json('response.json')[['id', 'name', 'areaname', 'volumn', 'leftspace', 'lat', 'lng']]
# ps_json = json.loads(parking_static_df.to_json(orient="records"))
# with open('parking_static.json', 'w') as f:
#     json.dump(ps_json, f)

parking_static_df = pd.DataFrame(data)[['id', 'name', 'areaname', 'volumn', 'leftspace', 'lat', 'lng']]
Base = declarative_base()
engine = create_engine(f"mysql+pymysql://thia01:thiits@localhost:3306/thi_db_1398", echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
#
parking_static_df.to_sql('parking_outer_static', engine, if_exists='append', index=False, chunksize=500, )
