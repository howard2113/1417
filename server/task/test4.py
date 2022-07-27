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

vd_1h_dynamic_res = requests.get(f'''http://223.200.72.159/cptapi/Traffic/api/VDOneHour?$filter=InfoDate%20eq%20%272021-12-01%27&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF''', headers={'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'})

print(vd_1h_dynamic_res)
