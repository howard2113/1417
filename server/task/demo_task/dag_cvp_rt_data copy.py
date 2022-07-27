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


def start():
    cfg = json.load(open(f"config/config.json", 'r'))
    Base = declarative_base()
    engine = create_engine(cfg['db'], echo=True)
    DB_session = sessionmaker(engine)
    db_session = DB_session()
    Base.metadata.create_all(engine)
    now = datetime.now()

    file_path0 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\people_24hr\cvp_rt_grid_data_202110220923.csv"
    rt_static_df = pd.read_csv(file_path0)[['gid', 'lat', 'lon']]

    '''
    hinet_cvp_rt_data_20211010000000.csv    hinet_cvp_rt_data_20211010010000.csv     hinet_cvp_rt_data_20211010020000.csv       hinet_cvp_rt_data_20211010030000.csv
    hinet_cvp_rt_data_20211010040000.csv    hinet_cvp_rt_data_20211010050000.csv     hinet_cvp_rt_data_20211010060000.csv       hinet_cvp_rt_data_20211010070000.csv
    hinet_cvp_rt_data_20211010080000.csv    hinet_cvp_rt_data_20211010090000.csv     hinet_cvp_rt_data_20211010100000.csv       hinet_cvp_rt_data_20211010110000.csv
    hinet_cvp_rt_data_20211010120000.csv    hinet_cvp_rt_data_20211010130000.csv     hinet_cvp_rt_data_20211010140000.csv       hinet_cvp_rt_data_20211010150000.csv
    hinet_cvp_rt_data_20211010160000.csv    hinet_cvp_rt_data_20211010170000.csv     hinet_cvp_rt_data_20211010180000.csv       hinet_cvp_rt_data_20211010190100.csv
    hinet_cvp_rt_data_20211010200000.csv    hinet_cvp_rt_data_20211010210000.csv     hinet_cvp_rt_data_20211010220000.csv       hinet_cvp_rt_data_20211010230000.csv
    
    new_cvp_rt_df = pd.json_normalize(new_cvp_rt_list)[['Gid', 'Population', 'Lat', 'Lon', 'SrcUpdateTime']]
    new_cvp_rt_df.rename(columns={"Gid": "gid", "Population": "population", "Lat": "lat", "Lon": "lon", "SrcUpdateTime": "src_time"}, inplace=True)
    '''
    file_list = ['hinet_cvp_rt_data_20211010000000.csv', 'hinet_cvp_rt_data_20211010010000.csv', 'hinet_cvp_rt_data_20211010020000.csv', 'hinet_cvp_rt_data_20211010030000.csv',
                 'hinet_cvp_rt_data_20211010040000.csv', 'hinet_cvp_rt_data_20211010050000.csv', 'hinet_cvp_rt_data_20211010060000.csv', 'hinet_cvp_rt_data_20211010070000.csv',
                 'hinet_cvp_rt_data_20211010080000.csv', 'hinet_cvp_rt_data_20211010090000.csv', 'hinet_cvp_rt_data_20211010100000.csv', 'hinet_cvp_rt_data_20211010110000.csv',
                 'hinet_cvp_rt_data_20211010120000.csv', 'hinet_cvp_rt_data_20211010130000.csv', 'hinet_cvp_rt_data_20211010140000.csv', 'hinet_cvp_rt_data_20211010150000.csv',
                 'hinet_cvp_rt_data_20211010160000.csv', 'hinet_cvp_rt_data_20211010170000.csv', 'hinet_cvp_rt_data_20211010180000.csv', 'hinet_cvp_rt_data_20211010190100.csv',
                 'hinet_cvp_rt_data_20211010200000.csv', 'hinet_cvp_rt_data_20211010210000.csv', 'hinet_cvp_rt_data_20211010220000.csv', 'hinet_cvp_rt_data_20211010230000.csv']
    for cvp_rt_file in file_list:

        header = ["ApiID", "Status", "Msg", "Name", "Gid", "Population", "DataTime", "SrcUpdateTime", "UpdateTime", "InfoTime", "InfoDate"]
        file_path1 = f"D:/desktop/1398高雄新一代ITS設計與實作計畫/db_bk1010/people_24hr/{cvp_rt_file}"
        new_cvp_rt_df = pd.read_csv(file_path1, index_col=False, header=None, names=header, sep='\t')[['Gid', 'Population', 'SrcUpdateTime']]
        new_cvp_rt_df.rename(columns={"Gid": "gid", "Population": "population", "SrcUpdateTime": "src_time"}, inplace=True)
        new_cvp_rt_df = pd.merge(new_cvp_rt_df, rt_static_df, on='gid', how='inner')
        new_cvp_rt_df['gid'] = new_cvp_rt_df.gid.astype(str)
        # 更新人潮網格資料
        for idx, new_cvp_rt_data in new_cvp_rt_df.iterrows():
            default_data = {'gid': new_cvp_rt_data['gid'], 'population': new_cvp_rt_data['population'], 'lat': new_cvp_rt_data['lat'], 'lon': new_cvp_rt_data['lon'], 'src_time': new_cvp_rt_data['src_time']}
            update_dict = {'population': new_cvp_rt_data['population'], 'src_time': new_cvp_rt_data['src_time']}
            sql_str = sql_insert_if_not_exist('cvp_rt_grid_data', default_data, ['gid', 'src_time'], update_dict)
            db_session.execute(sql_str)

        # 更新人潮區域統計資料
        sub_grid_area_df = pd.read_sql(f"SELECT * FROM sub_grid_area", con=engine)
        merge_df = pd.merge(new_cvp_rt_df, sub_grid_area_df, on='gid', how='inner')
        group_data = merge_df.groupby('name')

        for name, g_df in group_data:
            last_row = g_df.iloc[-1]
            default_data = {'name': name, 'count': g_df['population'].sum(), 'src_time': last_row['src_time']}
            sql_str = sql_insert_if_not_exist('sub_grid_count', default_data, ['name'], {'count': g_df['population'].sum(), 'src_time': last_row['src_time']})
            db_session.execute(sql_str)

    db_session.commit()


start()
