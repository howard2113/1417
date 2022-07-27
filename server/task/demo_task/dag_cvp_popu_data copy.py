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
from oauth2client.service_account import ServiceAccountCredentials as SAC
from utils.sql_build import sql_insert_if_not_exist, sql_update

# 設定資料庫
cfg = json.load(open(f"config/config.json", 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
now = datetime.now()
now = datetime.strptime('2021-10-10 23:59:59', '%Y-%m-%d %H:%M:%S')
day_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
day_end = now.replace(hour=23, minute=59, second=59)

_default_data = {'name': '', 'count': 0, 'h0': 0, 'h1': 0, 'h2': 0, 'h3': 0, 'h4': 0, 'h5': 0, 'h6': 0, 'h7': 0, 'h8': 0,
                 'h9': 0, 'h10': 0, 'h11': 0, 'h12': 0, 'h13': 0, 'h14': 0, 'h15': 0, 'h16': 0, 'h17': 0, 'h18': 0,
                 'h19': 0, 'h20': 0, 'h21': 0, 'h22': 0, 'h23': 0, 'src_time': ''}

hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']


def start():
    # cvp_twrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpTwrtData?$format=json''', headers=cfg['iis_api_header'])
    # print('cvp_twrt_res', cvp_twrt_res)
    # cvp_twrt_str = cvp_twrt_res.content.decode('utf-8')
    # cvp_twrt_list = json.loads(cvp_twrt_str)
    # cvp_twrt_df = pd.json_normalize(cvp_twrt_list)[['Name', 'Population']]
    
    '''
    .csv    .csv    .csv    .csv    .csv"
    .csv    .csv    .csv    .csv    .csv"
    .csv    .csv    .csv    .csv"
    '''
    header = ["ApiID", "Status", "Msg", "Name", "Population", "Male", "Female", "Age0019", "Age2029", "Age3039", "Age4049", "Age5059", "Age6099", "Nation", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "M", "N", "O", "P", "Q", "T", "U", "V", "W", "X", "Z", "North", "South", "West", "East", "NorthEast", "NorthWest", "SouthEast", "SouthWest", "DataTime", "SrcUpdateTime", "UpdateTime", "InfoTime", "InfoDate"]
    file_path1 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\people_24hr\hinet_cvp_twrtdata_20211010095000.csv"
    cvp_twrt_df = pd.read_csv(file_path1, index_col=False, header=None, names=header, sep='\t')[['Name', 'Population']]
    cvp_twrt_df.rename(columns={"Name": "name", "Population": "count"}, inplace=True)

    # new_cvp_popu_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/HinetCvpPopulation50?$format=json''', headers=cfg['iis_api_header'])
    # print('new_cvp_popu_res', new_cvp_popu_res)
    # new_cvp_popu_str = new_cvp_popu_res.content.decode('utf-8')
    # new_cvp_popu_list = json.loads(new_cvp_popu_str)
    # new_cvp_popu_df = pd.json_normalize(new_cvp_popu_list)[['EvName', 'Allcnt', 'SrcUpdateTime']]

    '''
    .csv    .csv    .csv    .csv    .csv"
    .csv    .csv    .csv    .csv    .csv"
    .csv    .csv    .csv    .csv    .csv"
    '''
    header = ["ApiID", "Status", "Msg", "EvName", "DataDate", "Allcnt", "Male", "Female", "Age19", "Age29", "Age39", "Age49", "Age59", "Age60", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "M", "N", "O", "P", "Q", "T", "U", "V", "W", "X", "Z", "SrcUpdateTime", "UpdateTime", "InfoTime", "InfoDate"]
    file_path2 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\people_24hr\hinet_cvp_population50_20211010090000.csv"
    new_cvp_popu_df = pd.read_csv(file_path2, index_col=False, header=None, names=header, sep='\t')[['EvName', 'Allcnt', 'SrcUpdateTime']]
    new_cvp_popu_df.rename(columns={"EvName": "name", "Allcnt": "total_count", "SrcUpdateTime": "src_time"}, inplace=True)
    new_cvp_popu_df = pd.merge(new_cvp_popu_df, cvp_twrt_df, on='name', how='inner')

    for idx, api_cvp_popu_data in new_cvp_popu_df.iterrows():
        default_data = _default_data.copy()
        default_data['name'] = api_cvp_popu_data['name']
        default_data[hour_map[now.hour]] = api_cvp_popu_data['total_count']
        default_data['count'] = api_cvp_popu_data['count']
        default_data['src_time'] = api_cvp_popu_data['src_time']
        src_datetime = datetime.strptime(api_cvp_popu_data['src_time'], '%Y-%m-%d %H:%M:%S')
        update_dict = {hour_map[src_datetime.hour]: api_cvp_popu_data['total_count'], 'count': api_cvp_popu_data['count'], 'src_time': api_cvp_popu_data['src_time'], 'update_time': now}
        for idx_hr, col_hr in enumerate(hour_map):
            if idx_hr > now.hour:
                update_dict[col_hr] = -1
        sql_str = sql_insert_if_not_exist('cvp_popu_data', default_data, ['name'], update_dict)
        db_session.execute(sql_str)

    db_session.commit()


start()
