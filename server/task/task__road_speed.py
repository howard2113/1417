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

vd_road_static_df = pd.read_sql("SELECT * FROM road_static_vd;", con=engine)
gvp_road_static_df = pd.read_sql("SELECT * FROM road_static_gvp;", con=engine)
# last_record_time = datetime.strptime('2021-08-02 00:00:00', '%Y-%m-%d %H:%M:%S')  # for test
delta_5m_dt = timedelta(minutes=5)
update_minute_list = [0, 10, 20, 30, 40, 50]
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']
r_dynamic_speed_df = pd.read_sql(f"SELECT * FROM road_dynamic_speed", con=engine)
last_time_minute = -1
while True:
    now = datetime.now()
    now = now.replace(second=0, microsecond=0)
    print('now:', now)
    if now.minute in update_minute_list and now.minute != last_time_minute:
        # if now.minute in update_minute_list and now.minute != last_time_minute or True: # for dev
        # ==========VD==========
        for index, vd_row in vd_road_static_df.iterrows():
            if len(r_dynamic_speed_df[r_dynamic_speed_df['id'] == vd_row['id']].index) <= 0:
                r_dynamic_speed_df = r_dynamic_speed_df.append({'id': vd_row['id'], 'area_name': vd_row['area_name'], 'name': vd_row['name'], 'dev': 0, 'tti': -1, 'h0': -1, 'h1': -1, 'h2': -1,
                                                                'h3': -1, 'h4': -1, 'h5': -1, 'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1,
                                                                'h14': -1, 'h15': -1, 'h16': -1, 'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': now, 'update_time': now}, ignore_index=True)
            if now.hour == 0 and now.minute == 0:
                r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == vd_row['id'], hour_map)] = -1
            for hour in range(24):
                if now.hour >= hour:
                    r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == vd_row['id']), hour_map[hour]] = random.randrange(20, 50)
                    r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == vd_row['id']), 'tti'] = random.random()

        # ==========GVP==========
        for index, gvp_row in gvp_road_static_df.iterrows():
            if len(r_dynamic_speed_df[r_dynamic_speed_df['id'] == gvp_row['id']].index) <= 0:
                r_dynamic_speed_df = r_dynamic_speed_df.append({'id': gvp_row['id'], 'area_name': gvp_row['area_name'], 'name': gvp_row['name'], 'dev': 1, 'tti': -1, 'h0': -1, 'h1': -1, 'h2': -1,
                                                                'h3': -1, 'h4': -1, 'h5': -1, 'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1,
                                                                'h14': -1, 'h15': -1, 'h16': -1, 'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': now, 'update_time': now}, ignore_index=True)
            if now.hour == 0 and now.minute == 0:
                r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == gvp_row['id'], hour_map)] = -1

            for hour in range(24):
                if now.hour >= hour:
                    r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == gvp_row['id']), hour_map[hour]] = random.randrange(20, 50)
                    r_dynamic_speed_df.loc[(r_dynamic_speed_df['id'] == gvp_row['id']), 'tti'] = random.random()

        engine.execute("DELETE FROM road_dynamic_speed")
        r_dynamic_speed_df.to_sql('road_dynamic_speed', engine, if_exists='append', index=False, chunksize=500, )

        last_time_minute = now.minute

    time.sleep(10)
