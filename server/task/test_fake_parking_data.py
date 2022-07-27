import numpy as np
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

# parking_static_url = "https://ptps.tbkc.gov.tw/api/GetLotSpace"
# parking_static_df = pd.read_json('response.json')[['id', 'name', 'volumn']]

# # set blank data for test
# total_res_df = pd.DataFrame(columns=['id', 'name', 'total_leftspace', 'hour', 'days'])
# for index, row in parking_static_df.iterrows():
#     for hour in range(24):
#         '''
#         name = fields.String(required=True)
#         total_leftspace = fields.Integer(required=True)
#         hour = fields.Integer(required=True)
#         days = fields.Integer(required=True)
#         '''
#         blank_data = {'id': row['id'], 'name': row['name'], 'total_leftspace': 0, 'hour': hour, 'days': 0}
#         print(blank_data, 'add ok!')
#         total_res_df = total_res_df.append(blank_data, ignore_index=True)
#
# total_res_df.to_sql('parking_outer_left_space_24h_mean', engine, if_exists='append', index=False, chunksize=500, )

# generate fake data
# sql_str = "SELECT * FROM parking_outer_left_space_24h_mean;"
# total_old_df = pd.read_sql(sql_str, con=engine)
# # print(total_old_df)
# for day in range(60):
#     total_res_df = pd.DataFrame(columns=['id', 'name', 'total_leftspace', 'hour', 'days'])
#     for index, row in parking_static_df.iterrows():
#         for hour in range(24):
#             _id = row["id"]
#             if row['volumn'] > 0:
#                 total_old_df.loc[(total_old_df["id"] == _id) & (total_old_df["hour"] == hour), 'total_leftspace'] += random.randrange(int(row['volumn'] / 2), row['volumn'])
#             total_old_df.loc[(total_old_df["id"] == _id) & (total_old_df["hour"] == hour), 'days'] += 1
#             print(_id, 'add ok!')
#
#     total_old_df.to_sql('parking_outer_left_space_24h_mean', engine, if_exists='replace', index=False, chunksize=500, )


'''
    ##dynamic
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    leftspace = db.Column(db.Integer)
    updatetime = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True)
    ========================================================================================
    ##mean
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    total_leftspace = db.Column(db.Integer)
    hour = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.Integer)
'''
# #
# # get_lot_space_url = "https://ptps.tbkc.gov.tw/api/GetLotSpace"
# # ApiKey = '9bf2beb46d6afc93384c95b2d86d4e61f7b558bc9db110fc3a951ced0ed66ed7'
# #
# # parking_static_df = pd.read_sql("SELECT * FROM parking_outer_static;", con=engine)
# # parking_24h_mean_df = pd.read_sql("SELECT * FROM parking_outer_left_space_24h_mean;", con=engine)
# #
# # # set blank data for test
# #
# # last_record_time = datetime.now()
# # update_minute_list = [0, 10, 20, 30, 40, 50]
# #
# # while True:
# #     now = datetime.now()
# #     print('now:', now)
# #     if now.minute in update_minute_list:
# #         parking_dynamic_df = pd.DataFrame(columns=['id', 'name', 'leftspace', 'updatetime'])
# #         for index, row in parking_static_df.iterrows():
# #             post_data = json.dumps({"ApiKey": ApiKey, "LotId": row['id']})
# #             res = requests.post(get_lot_space_url, json=post_data, headers={"Content-Type": "application/json"})
# #             leftspace = int(json.loads(res.text))
# #             dynamic_dict = {'id': row['id'], 'name': row['name'], 'leftspace': leftspace, 'updatetime': now}
# #
# #             parking_24h_mean_df.loc[(parking_24h_mean_df["id"] == row['id']) & (parking_24h_mean_df["hour"] == now.hour), 'total_leftspace'] += leftspace
# #             parking_24h_mean_df.loc[(parking_24h_mean_df["id"] == row['id']) & (parking_24h_mean_df["hour"] == now.hour), 'times'] += 1
# #
# #             print(dynamic_dict, 'add ok!')
# #             print(now)
# #             parking_dynamic_df = parking_dynamic_df.append(dynamic_dict, ignore_index=True)
# #         parking_24h_mean_df.to_sql('parking_outer_left_space_24h_mean', engine, if_exists='replace', index=False, chunksize=500, )
# #         parking_dynamic_df.to_sql('parking_outer_left_space_dynamic', engine, if_exists='replace', index=False, chunksize=500, )
# #
# #     time.sleep(60)
#
# '''
# parking_outer_left_space_dynamic
# id = db.Column(db.String(10), primary_key=True)
# name = db.Column(db.String(50))
# hour = db.Column(db.Integer)
# leftspace = db.Column(db.Integer)
# updatetime = db.Column(db.DateTime, server_default=db.func.now(), primary_key=True)
# '''

# VD & GVP set fake dynamic data with mean for test
parking_static_df = pd.read_sql("SELECT * FROM parking_outer_static;", con=engine)
update_minute_list = [0, 10, 20, 30, 40, 50]
parking_dynamic_df = pd.DataFrame(columns=['id', 'name', 'hour', 'leftspace'])

now = datetime.now()
for index, row in parking_static_df.iterrows():
    for hour in range(24):
        if now.hour >= hour and row['volumn'] > 0:
            leftspace = random.randrange(int(row['volumn'] / 8), row['volumn'])
        else:
            leftspace = -1
        fake_data = {'id': row['id'], 'name': row['name'], 'hour': hour, 'leftspace': leftspace}
        parking_dynamic_df = parking_dynamic_df.append(fake_data, ignore_index=True)
        print(fake_data, 'add ok')
engine.execute("DELETE FROM parking_outer_left_space_dynamic")
parking_dynamic_df.to_sql('parking_outer_left_space_dynamic', engine, if_exists='append', index=False, chunksize=500, dtype={"hour": Integer(), "leftspace": Integer()})



while True:
    now = datetime.now()
    print('now:', now)
    if now.minute in update_minute_list:
    # if now.minute in update_minute_list or True: # for test
        for index, row in parking_static_df.iterrows():
            _id = row["id"]
            if row['volumn'] > 0:
                leftspace = random.randrange(int(row['volumn'] / 8), row['volumn'])
                parking_dynamic_df.loc[(parking_dynamic_df["id"] == _id) & (parking_dynamic_df["hour"] == now.hour), 'leftspace'] = leftspace
                parking_dynamic_df.loc[(parking_dynamic_df["id"] == _id) & (parking_dynamic_df["hour"] > now.hour), 'leftspace'] = -1
        engine.execute("DELETE FROM parking_outer_left_space_dynamic")
        parking_dynamic_df.to_sql('parking_outer_left_space_dynamic', engine, if_exists='append', index=False, chunksize=500, dtype={"hour": Integer(), "leftspace": Integer()})

    time.sleep(60)
