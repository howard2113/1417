import time
import numpy as np
import json
import gspread
import requests
import pandas as pd
from datetime import datetime, timedelta
from util.sql_build import sql_insert_if_not_exist, sql_update
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from oauth2client.service_account import ServiceAccountCredentials as SAC

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
now = datetime.now()

api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

'''
id,area_name,name,dev, speed,tti,h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16,h17,h18,h19,h20,h21,h22,h23,src_time,update_time
'''

_default_data_speed = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 1, 'tti': -1, 'speed': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                      'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                      'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

#http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/GVPLiveTraffic?$top=30&$format=json
def start():

    # 撈取本機GVP section資料
    gvp_section_df = pd.read_sql(f"SELECT * FROM road_section_gvp", con=engine)
    gvp_section_df['total_name'] = gvp_section_df['name'] + '(' + gvp_section_df['start_pos'] + '~' + gvp_section_df['end_pos'] + ')' + gvp_section_df['direction']
    gvp_section_df['SectionID'] = gvp_section_df['id']

    # 撈取gvp 動態資料
    gvp_dynamic_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/GVPLiveTraffic?$format=json''', headers=api_headers)
    gvp_dynamic_str = gvp_dynamic_res.content.decode('utf-8')
    gvp_dynamic_list = json.loads(gvp_dynamic_str)
    gvp_dynamic_df = pd.DataFrame(gvp_dynamic_list)[['SectionID', 'TravelSpeed', 'DataCollectTime', 'Tti']]
    m_gvp_dynamic_df = pd.merge(gvp_dynamic_df, gvp_section_df, on='SectionID', how='left')
    m_gvp_dynamic_df.sort_values('DataCollectTime', inplace=True)
    # m_gvp_dynamic_df.drop_duplicates(subset=['SectionID'], keep='last', inplace=True)
    m_gvp_dynamic_df.dropna(inplace=True)
    # 分時
    for idx, gvp_data in m_gvp_dynamic_df.iterrows():
        # 速度
        src_time = datetime.strptime(gvp_data['DataCollectTime'], '%Y-%m-%d %H:%M:%S')
        if src_time.hour==now.hour:
            default_data_speed = _default_data_speed.copy()
            default_data_speed['id'] = gvp_data['id']
            default_data_speed['l_id'] = gvp_data['id']
            default_data_speed['name'] = gvp_data['total_name']
            default_data_speed['area_name'] = gvp_data['area_name']
            default_data_speed['tti'] = gvp_data['Tti']
            default_data_speed['speed'] = gvp_data['TravelSpeed']
            default_data_speed[hour_map[src_time.hour]] = gvp_data['TravelSpeed']
            default_data_speed['src_time'] = gvp_data['DataCollectTime']
            update_dict = {hour_map[src_time.hour]: gvp_data['TravelSpeed'], 'speed': default_data_speed['speed'], 'tti': default_data_speed['tti'], 'src_time': gvp_data['DataCollectTime'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('road_dynamic_speed', default_data_speed, ['l_id', 'id'], update_dict)
            db_session.execute(sql_str)

    db_session.commit()


start()




