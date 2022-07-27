import pandas as pd
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


'''
bill_no, lac_code, city, start_date, car_no, start_time, end_time, park_time_unit, park_mins, bill_count, amount, user_pay, pay_status, pay_type, fee_type, update_time
'''

grid_statics_df = pd.read_sql(f"SELECT * FROM grid_statics", con=engine)
official_id_group = grid_statics_df.groupby(['official_id'])
for official_id,  df in official_id_group:
    loc_no = len(df.index)
    rom_name = df['rom_name'].iloc[0]
    sql_str = sql_insert('road_statics', {'rom_name': rom_name, 'official_id': official_id, 'loc_no': loc_no})
    print(loc_no)
    db_session.execute(sql_str)
db_session.commit()





# acer_df = pd.read_csv(r"D:\desktop\1393宏碁智慧停車場\grid_statics_202112090857.csv")
# acer_df['log_time'] = pd.to_datetime(acer_df['log_time'])
# acer_df['end_date'] = pd.to_datetime(acer_df['end_date'])
# acer_df['update_time'] = pd.to_datetime(acer_df['update_time'])
# acer_df['log_time'] = acer_df['log_time']-timedelta(hours=8)
# acer_df['end_date'] = acer_df['end_date']-timedelta(hours=8)
# acer_df['update_time'] = acer_df['update_time']-timedelta(hours=8)
# acer_df.drop(['park_hrs'], axis=1, inplace=True)

# print(acer_df)

# acer_df.to_sql('grid_statics', engine, if_exists='append', index=False, chunksize=500, )

#
# test_data = {"bill_no": "test", "lac_code": "0043-001", "city": "台北", "start_date": "2021-12-20T00:00:00+8", "car_no": "ARZ-3335", "start_time": "2021-12-20T21:00:00Z",
#              "end_time": "2021-12-20T22:00:00Z", "park_time_unit": 1, "park_mins": 60, "bill_count": 2, "amount": 100, "user_pay": 1, "pay_status": 1,
#              "pay_type": 1, "fee_type": 1}
#
# '''
# bill_no,lac_code,city,start_date,car_no,start_time,end_time,park_time_unit,park_mins,bill_count,amount,user_pay,pay_status,pay_type,fee_type,update_time,park_hrs
# '''
#
# sql_str = sql_insert('parking_bills', test_data)
# db_session.execute(sql_str)
# db_session.commit()


