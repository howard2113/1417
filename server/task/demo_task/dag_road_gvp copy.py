import os
import time
import pandas as pd
import requests
import logging
import json
import gspread
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime, timedelta
from utils.sql_build import sql_insert_if_not_exist

# 設定資料庫
cfg = json.load(open(f"config/config.json", 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
now = datetime.now()

api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

_default_data_speed = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 1, 'tti': -1, 'speed': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                       'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                       'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']


def start():
    # 撈取本機GVP section資料
    gvp_section_df = pd.read_sql(f"SELECT * FROM road_section_gvp", con=engine)
    gvp_section_df['total_name'] = gvp_section_df['name'] + '(' + gvp_section_df['start_pos'] + '~' + gvp_section_df['end_pos'] + ')' + gvp_section_df['direction']
    gvp_section_df['SectionID'] = gvp_section_df['id']

    # 撈取gvp 動態資料
    # gvp_dynamic_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/GVPLiveTraffic?$format=json''', headers=api_headers)
    # gvp_dynamic_str = gvp_dynamic_res.content.decode('utf-8')
    # gvp_dynamic_list = json.loads(gvp_dynamic_str)
    # gvp_dynamic_df = pd.DataFrame(gvp_dynamic_list)[['SectionID', 'TravelSpeed', 'DataCollectTime', 'Tti']]
    '''
    "D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\roadmgmt_road_google_202110221026.csv"
    "seq_id","road_id","length","ttime","speed","speed_th1","speed_th2","moe_level","cron_id","datasource_id","datasource_type","recv_time"
    500261  ,kao_0064 ,1141    ,134    ,30.7   ,21.7068    ,18.3673    ,1          ,13       ,15             ,Google           ,2021-10-10 09:15:00.000
    
    
    "road_id","start_x","start_y","end_x","end_y","waypoints","length","ttime_freeflow_his","ttime_freeflow","ttime_th1","ttime_th2","speed_freeflow_his","speed_freeflow","speed_th1","speed_th2","polyline_original","polyline"
kao_0001,"120.2701","22.62404","120.27503","22.62122","via:22.622630007229922,120.272565",596.0,78.0000,78.0000,120.0000,141.8182,27.4615,27.4615,17.8500,15.1038,owaiCiga}U`BmDpAgCrBiEnBeEjCqFV[,"120.270105,22.624036 120.270974,22.623546 120.271654,22.623136 120.272665,22.622556 120.273655,22.621996 120.27486,22.621299 120.274997,22.621182"

    
    '''
    file_path0 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\roadmgmt_road_google_202110221026.csv"
    freeflow_df = pd.read_csv(file_path0)[['road_id', 'speed_freeflow']]
    file_path1 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\roadmgmt_ttime_202110141219.csv"
    gvp_dynamic_df = pd.read_csv(file_path1)[['road_id', 'speed', 'recv_time']]
    m_gvp_dynamic_df = pd.merge(gvp_dynamic_df, freeflow_df, on='road_id', how='left')
    m_gvp_dynamic_df['SectionID'] = m_gvp_dynamic_df['road_id']
    m_gvp_dynamic_df = pd.merge(m_gvp_dynamic_df, gvp_section_df, on='SectionID', how='left')
    m_gvp_dynamic_df.sort_values('recv_time', inplace=True)
    m_gvp_dynamic_df.dropna(inplace=True)
    m_gvp_dynamic_df['recv_time'] = pd.to_datetime(m_gvp_dynamic_df['recv_time'])
    gvp_dynamic_group = m_gvp_dynamic_df.groupby(["SectionID", pd.Grouper(key='recv_time', freq='1h')])
    print(gvp_dynamic_group)
    for name, df in gvp_dynamic_group:
        print(name, df)
        last_row = df.iloc[-1]
        default_data_speed = _default_data_speed.copy()
        default_data_speed['id'] = last_row['road_id']
        default_data_speed['l_id'] = last_row['road_id']
        default_data_speed['name'] = last_row['total_name']
        default_data_speed['area_name'] = last_row['area_name']
        default_data_speed['tti'] = last_row['speed']/last_row['speed_freeflow']
        default_data_speed['speed'] = last_row['speed']
        default_data_speed[hour_map[last_row['recv_time'].hour]] = last_row['speed']
        default_data_speed['src_time'] = last_row['recv_time']
        update_dict = {hour_map[last_row['recv_time'].hour]: last_row['speed'], 'speed': default_data_speed['speed'], 'tti': default_data_speed['tti'], 'src_time': last_row['recv_time'], 'update_time': now}

        sql_str = sql_insert_if_not_exist('road_dynamic_speed', default_data_speed, ['l_id', 'id'], update_dict)
        db_session.execute(sql_str)

    db_session.commit()

    # # 分時
    # for idx, gvp_data in m_gvp_dynamic_df.iterrows():
    #     # 速度
    #     src_time = datetime.strptime(gvp_data['DataCollectTime'], '%Y-%m-%d %H:%M:%S')
    #     if src_time.hour == now.hour:
    #         default_data_speed = _default_data_speed.copy()
    #         default_data_speed['id'] = gvp_data['road_id']
    #         default_data_speed['l_id'] = gvp_data['road_id']
    #         default_data_speed['name'] = gvp_data['total_name']
    #         default_data_speed['area_name'] = gvp_data['area_name']
    #         default_data_speed['tti'] = gvp_data['Tti']
    #         default_data_speed['speed'] = gvp_data['TravelSpeed']
    #         default_data_speed[hour_map[src_time.hour]] = gvp_data['TravelSpeed']
    #         default_data_speed['src_time'] = gvp_data['DataCollectTime']
    #         update_dict = {hour_map[src_time.hour]: gvp_data['TravelSpeed'], 'speed': default_data_speed['speed'], 'tti': default_data_speed['tti'], 'src_time': gvp_data['DataCollectTime'], 'update_time': now}
    #         for idx_hr, col_hr in enumerate(hour_map):
    #             if idx_hr > now.hour:
    #                 update_dict[col_hr] = -1
    #         sql_str = sql_insert_if_not_exist('road_dynamic_speed', default_data_speed, ['l_id', 'id'], update_dict)
    #         db_session.execute(sql_str)
    #
    # db_session.commit()


start()
