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


def start():
    cfg = json.load(open(f"config/config.json", 'r'))
    Base = declarative_base()
    engine = create_engine(cfg['db'], echo=True)
    DB_session = sessionmaker(engine)
    db_session = DB_session()
    Base.metadata.create_all(engine)
    now = datetime.now()
    hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']

    # mrt_res = requests.get(f'''{cfg['iis_api_url']}/Other/api/MrtTransCount?$format=json''', headers=cfg['iis_api_header'])
    # print('mrt_res', mrt_res)
    # mrt_str = mrt_res.content.decode('utf-8')
    # mrt_list = json.loads(mrt_str)
    # mrt_df = pd.json_normalize(mrt_list)
    '''
    '''
    header = ["TicketType", "TrainType", "StationNo", "StationName", "TranscationDate", "EnterCount", "ExitCount", "SrcUpdateTime", "UpdateTime", "InfoTime", "InfoDate"]
    file_path1 = r"D:\desktop\1398高雄新一代ITS設計與實作計畫\db_bk1010\捷運即時分刻運量\2020-10-10\mrt_trans_count_20211010235500.csv"
    mrt_df = pd.read_csv(file_path1, index_col=False, header=None, names=header, sep='\t')[['TrainType', 'StationName', 'EnterCount', 'ExitCount', 'SrcUpdateTime', 'TranscationDate']]
    mrt_df.rename(columns={"TrainType": "train_type", "StationName": "station_name", "EnterCount": "enter", "ExitCount": "exit", "SrcUpdateTime": "src_time", "TranscationDate": "transaction_date"}, inplace=True)

    station_group = mrt_df.groupby('station_name')

    mrt_df["enter_count"] = station_group["enter"].transform('sum')
    mrt_df["exit_count"] = station_group["exit"].transform('sum')
    mrt_df.drop_duplicates(subset=['station_name'], keep='last', inplace=True)
    mrt_df = mrt_df[['train_type', 'station_name', 'enter', "enter_count", "exit_count", 'exit', 'src_time', 'transaction_date']]
    mrt_df['enter_rank'] = 0
    mrt_df['exit_rank'] = 0
    engine.execute("DELETE FROM mrt_count")
    mrt_df.to_sql('mrt_count', engine, if_exists='append', index=False, chunksize=500, )


start()