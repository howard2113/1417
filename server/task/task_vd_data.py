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

# 設定google api
google_key_json = 'alpine-sentry-325407-58063405de05.json'  # Json 的單引號內容請改成個人下載的金鑰
google_sheet_url = ['https://spreadsheets.google.com/feeds']
g_connect = SAC.from_json_keyfile_name(google_key_json, google_sheet_url)
g_sheets = gspread.authorize(g_connect)
api_headers = {'accept': '*/*', 'Authorization': 'FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'}

'''
id,area_name,name,dev,tti,h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16,h17,h18,h19,h20,h21,h22,h23,src_time,update_time

id,area_name,name,dev,pcu,h0,h1,h2,h3,h4,h5,h6,h7,h8,h9,h10,h11,h12,h13,h14,h15,h16,h17,h18,h19,h20,h21,h22,h23,src_time,update_time
'''

_default_data_flow = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 0, 'pcu': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                      'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                      'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

_default_data_speed = {'id': '', 'l_id': '', 'area_name': '暫無', 'name': '', 'dev': 0, 'tti': -1, 'speed': -1, 'h0': -1, 'h1': -1, 'h2': -1, 'h3': -1, 'h4': -1, 'h5': -1,
                       'h6': -1, 'h7': -1, 'h8': -1, 'h9': -1, 'h10': -1, 'h11': -1, 'h12': -1, 'h13': -1, 'h14': -1, 'h15': -1, 'h16': -1,
                       'h17': -1, 'h18': -1, 'h19': -1, 'h20': -1, 'h21': -1, 'h22': -1, 'h23': -1, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']
'''
L_6194200200040E  公園二路(大智路~五福四路)往東
L_6194200600040E  公園二路(五福四路~大智路)往西
L_6194200200020E  公園二路(七賢三路~大勇路)往東
L_6194200600020E  公園二路(大勇路~七賢三路)往西
L_6193620300050E  五福四路(大智路~公園二路)往東
L_6193620700050E  五福四路(公園二路~大智路)往西
L_6193620300030E  五福四路(七賢三路~大勇路)往東
L_6193620700030E  五福四路(大勇路~七賢三路)往西
'''


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

    # 更新VD靜態資料
    static_vd_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/VD/AuthorityCode/KHH?$format=json''', headers=api_headers)
    static_vd_str = static_vd_res.content.decode('utf-8')
    static_vd_list = json.loads(static_vd_str)
    static_vd_df = pd.json_normalize(static_vd_list)[['VDID', 'RoadName', 'PositionLat', 'PositionLon', 'RoadSection.Start', 'RoadSection.End', 'UpdateTime']]
    static_vd_df.rename(columns={"VDID": "id", "RoadName": "name", "PositionLat": "lat", "PositionLon": "lon", "RoadSection.Start": "start_pos", "RoadSection.End": "end_pos", "UpdateTime": 'src_time'}, inplace=True)
    engine.execute(f"DELETE FROM road_static_vd")
    static_vd_df.to_sql('road_static_vd', engine, if_exists='append', index=False, chunksize=500, )

    # 撈取API VD 小時資料
    vd_1h_dynamic_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/VDOneHour?$format=json''', headers=api_headers)
    vd_1h_dynamic_str = vd_1h_dynamic_res.content.decode('utf-8')
    vd_1h_dynamic_list = json.loads(vd_1h_dynamic_str)
    vd_1h_dynamic_df = pd.DataFrame(vd_1h_dynamic_list)[['VDID', 'LinkID', 'Speed', 'Tti', 'Pcu', 'SrcUpdateTime']]
    vd_1h_dynamic_df['LinkID'] = 'L_' + vd_1h_dynamic_df['LinkID']
    m_vd_dynamic_df = pd.merge(vd_1h_dynamic_df, vd_section_df, on='LinkID', how='left')[['VDID', 'area_name', 'total_name', 'LinkID', 'Speed', 'Tti', 'Pcu', 'SrcUpdateTime']]
    m_vd_dynamic_df.dropna(inplace=True)
    m_vd_dynamic_df.rename(columns={"VDID": "id", 'total_name': 'name', "LinkID": "l_id", "Speed": "speed", "Pcu": "pcu", "SrcUpdateTime": "src_time"}, inplace=True)
    m_vd_dynamic_df.sort_values('src_time', inplace=True)

    # 即時5分鐘
    vd_5m_dynamic_res = requests.get(f'''{cfg['iis_api_url']}/Traffic/api/VDFiveMin?$format=json''', headers=api_headers)
    vd_5m_dynamic_str = vd_5m_dynamic_res.content.decode('utf-8')
    vd_5m_dynamic_list = json.loads(vd_5m_dynamic_str)
    vd_5m_dynamic_df = pd.DataFrame(vd_5m_dynamic_list)[['VDID', 'LinkID', 'Speed', 'Tti', 'Pcu', 'SrcUpdateTime']]
    vd_5m_dynamic_df['LinkID'] = 'L_' + vd_5m_dynamic_df['LinkID']

    # 分時
    for idx, vd_data in m_vd_dynamic_df.iterrows():
        # 速度
        src_time = datetime.strptime(vd_data['src_time'], '%Y-%m-%d %H:%M:%S')
        if src_time.hour == now.hour:
            df_index = vd_5m_dynamic_df.index[vd_5m_dynamic_df['LinkID'] == vd_data['l_id']]
            default_data_speed = _default_data_speed.copy()
            default_data_speed['id'] = vd_data['id']
            default_data_speed['l_id'] = vd_data['l_id']
            default_data_speed['name'] = vd_data['name']
            default_data_speed['area_name'] = vd_data['area_name']
            default_data_speed[hour_map[src_time.hour]] = vd_data['speed']
            default_data_speed['speed'] = vd_5m_dynamic_df.loc[df_index, 'Speed'].values[0]
            default_data_speed['tti'] = vd_5m_dynamic_df.loc[df_index, 'Tti'].values[0]
            default_data_speed['src_time'] = vd_5m_dynamic_df.loc[df_index, 'SrcUpdateTime'].values[0]
            update_dict = {hour_map[src_time.hour]: vd_data['speed'], 'speed': default_data_speed['speed'], 'tti': default_data_speed['tti'], 'src_time': default_data_speed['src_time'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('road_dynamic_speed', default_data_speed, ['l_id', 'id'], update_dict)
            db_session.execute(sql_str)
            # 流量
            default_data_flow = _default_data_flow.copy()
            default_data_flow['id'] = vd_data['id']
            default_data_flow['l_id'] = vd_data['l_id']
            default_data_flow['name'] = vd_data['name']
            default_data_flow['area_name'] = vd_data['area_name']
            default_data_flow[hour_map[src_time.hour]] = vd_data['pcu']
            default_data_flow['pcu'] = vd_5m_dynamic_df.loc[df_index, 'Pcu'].values[0]
            default_data_flow['src_time'] = vd_5m_dynamic_df.loc[df_index, 'SrcUpdateTime'].values[0]
            update_dict = {hour_map[src_time.hour]: vd_data['pcu'], 'pcu': default_data_flow['pcu'], 'src_time': default_data_speed['src_time'], 'update_time': now}
            for idx_hr, col_hr in enumerate(hour_map):
                if idx_hr > now.hour:
                    update_dict[col_hr] = -1
            sql_str = sql_insert_if_not_exist('road_dynamic_flow', default_data_flow, ['l_id', 'id'], update_dict)
            db_session.execute(sql_str)

    db_session.commit()


start()
