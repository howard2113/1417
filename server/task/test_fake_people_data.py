import time
import pandas as pd
import requests
import json
import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

'''
  "name(場地名稱)" : "string",
  "data(資料[{時間:人數}])" : {
    "YYYY-MM-DD HH:mm:ss" : "int",
    "YYYY-MM-DD HH:mm:ss" : "int",
    "YYYY-MM-DD HH:mm:ss" : "int",
    ...
    =================================================
    name = db.Column(db.String(50))
    count = db.Column(db.Integer)
    updatetime = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True)
    =================================================
    start_time = db.Column(db.DateTime, primary_key=True)
    end_time = db.Column(db.DateTime)
'''

people_static_df = pd.read_sql("SELECT * FROM people_static;", con=engine)

# set blank data for test
total_res_df = pd.DataFrame(columns=['id', 'name', 'count'])
last_record_time = datetime.now()
update_minute_list = [0, 15, 30, 45]

now = datetime.strptime('2021-07-30 08:00:00', '%Y-%m-%d %H:%M:%S')  # for test
while True:
    if now > datetime.strptime('2021-08-03 20:00:00', '%Y-%m-%d %H:%M:%S'):
        print(now)
        total_res_df.to_sql('people_dynamic', engine, if_exists='append', index=False, chunksize=500, )
        break
    # now = datetime.now()
    if now.minute in update_minute_list or True:  # for test
    # if now.minute in update_minute_list:
        for index, row in people_static_df.iterrows():
            if row['end_time'] >= now >= row['start_time']:
                count = random.randrange(88, 1688)
                fake_data = {'name': row['name'], 'count': count, 'updatetime': now}
                print(fake_data, 'add ok!')
                print(now)
                total_res_df = total_res_df.append(fake_data, ignore_index=True)
    now = now + timedelta(minutes=15)
    # total_res_df.to_sql('people_dynamic', engine, if_exists='append', index=False, chunksize=500, )
