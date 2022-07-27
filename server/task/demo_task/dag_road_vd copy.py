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

_default_data_flow = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 0, 'pcu': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                      'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                      'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

_default_data_speed = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 0, 'tti': -1, 'speed': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                       'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                       'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']


def start():
    # 撈取本機VD section資料
    vd_section_df = pd.read_sql(f"SELECT * FROM road_section_vd", con=engine)
    vd_section_df['total_name'] = vd_section_df['name'] + '(' + vd_section_df['start_pos'] + '~' + vd_section_df['end_pos'] + ')' + vd_section_df['direction']
    vd_section_df['LinkID'] = vd_section_df['id']
    vd_section_df_idx = vd_section_df[vd_section_df['id'].isin(
        ['L_6192540200020E', 'L_6192540200070E', 'L_6192540600020E', 'L_6192540600070E', 'L_6193130000030E', 'L_6193130400030E',
         'L_6193150000050E', 'L_6193150400050E', 'L_6193160000030E', 'L_6193160000050E', 'L_6193160400030E', 'L_6193160400050E',
         'L_6193160400070E', 'L_6193600200050E', 'L_6193600600040E', 'L_6193620300030E', 'L_6193620300050E', 'L_6193620700030E',
         'L_6193620700050E', 'L_6194200200020E', 'L_6194200200040E', 'L_6194200600020E', 'L_6194200600040E', 'L_6198330000050E',
         'L_6198330000080E', 'L_6198330400050E', 'L_6198330400080E', 'L_6198340000060E', 'L_6198340400060E', 'L_6207700100040E'])]
    vd_section_df.drop(vd_section_df_idx.index, inplace=True)

    # 撈取API VD 小時資料
    # vd_1h_dynamic_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/VDOneHour?$format=json''', headers=api_headers)
    # vd_1h_dynamic_str = vd_1h_dynamic_res.content.decode('utf-8')
    # vd_1h_dynamic_list = json.loads(vd_1h_dynamic_str)
    # vd_1h_dynamic_df = pd.DataFrame(vd_1h_dynamic_list)[['VDID', 'LinkID', 'Speed', 'Tti', 'Pcu', 'SrcUpdateTime']]
    '''
    "vd_id","status","link_id"        ,"speed" ,"s_volume","t_volume","l_volume","m_volume","occ","tti","pcu","avg_pcu","data_collect_time"     ,"SrcUpdateTime"         ,"UpdateTime"            ,"InfoTime"              ,"InfoDate"
    V000301,        ,"6196790000020E" ,0.00    ,0         ,0         ,0         ,0         ,0.00 ,0.00 ,0.00 ,0.00     ,2021-10-10 00:00:00.000 ,2021-10-10 00:00:00.000 ,2021-10-10 00:02:30.000 ,2021-10-10 00:00:00.000 ,2021-10-10
    '''
    file_path1 = r'D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\vd_one_hour_202110141216.csv'
    vd_1h_dynamic_df = pd.read_csv(file_path1)[['vd_id', 'link_id', 'speed', 'tti', 'pcu', 'SrcUpdateTime']]
    vd_1h_dynamic_df['LinkID'] = 'L_' + vd_1h_dynamic_df['link_id']
    m_vd_dynamic_df = pd.merge(vd_1h_dynamic_df, vd_section_df, on='LinkID', how='left')[['vd_id', 'area_name', 'total_name', 'link_id', 'speed', 'tti', 'pcu', 'SrcUpdateTime']]
    m_vd_dynamic_df.dropna(inplace=True)
    m_vd_dynamic_df.rename(columns={"vd_id": "id", 'total_name': 'name', "link_id": "l_id", "SrcUpdateTime": "src_time"}, inplace=True)
    m_vd_dynamic_df.sort_values('src_time', inplace=True)

    # 分時
    for idx, vd_data in m_vd_dynamic_df.iterrows():
        # 速度
        src_time = datetime.strptime(vd_data['src_time'], '%Y-%m-%d %H:%M:%S.%f')

        default_data_speed = _default_data_speed.copy()
        default_data_speed['id'] = vd_data['id']
        default_data_speed['l_id'] = vd_data['l_id']
        default_data_speed['name'] = vd_data['name']
        default_data_speed['area_name'] = vd_data['area_name']
        default_data_speed[hour_map[src_time.hour]] = vd_data['speed']
        default_data_speed['speed'] = vd_data['speed']
        default_data_speed['tti'] = vd_data['tti']
        default_data_speed['src_time'] = vd_data['src_time']
        update_dict = {hour_map[src_time.hour]: vd_data['speed'], 'speed': default_data_speed['speed'], 'tti': default_data_speed['tti'], 'src_time': default_data_speed['src_time'], 'update_time': now}
        sql_str = sql_insert_if_not_exist('road_dynamic_speed', default_data_speed, ['l_id', 'id'], update_dict)
        db_session.execute(sql_str)
        # 流量
        default_data_flow = _default_data_flow.copy()
        default_data_flow['id'] = vd_data['id']
        default_data_flow['l_id'] = vd_data['l_id']
        default_data_flow['name'] = vd_data['name']
        default_data_flow['area_name'] = vd_data['area_name']
        default_data_flow[hour_map[src_time.hour]] = vd_data['pcu']
        default_data_flow['pcu'] = vd_data['pcu']
        default_data_flow['src_time'] = vd_data['src_time']
        update_dict = {hour_map[src_time.hour]: vd_data['pcu'], 'pcu': default_data_flow['pcu'], 'src_time': default_data_speed['src_time'], 'update_time': now}
        sql_str = sql_insert_if_not_exist('road_dynamic_flow', default_data_flow, ['l_id', 'id'], update_dict)
        db_session.execute(sql_str)

    db_session.commit()


start()
