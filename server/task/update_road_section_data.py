import os.path
import numpy as np
import time
import requests
import json
import random
import pandas as pd
import tempfile
from util import pd_util
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float, BigInteger, REAL
from util.database import mysql2csv




# cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
# engine = create_engine('postgresql://root:thi168168@localhost:5432/kh_its_1398', echo=True)
engine = create_engine('postgresql://root:thi168168@220.130.185.36:5432/kh_its_1398_v3', echo=True)
# engine = create_engine(f"mysql+pymysql://thia01:thiits@220.130.185.36:3306/dev_1398", echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)
#
# engine.execute(f"DELETE FROM road_section_vd")
# now = datetime.now()
# intercity_bridge_info_df = pd.read_csv(r"D:\desktop\1398高雄新一代ITS設計與實作計畫\vd_section_v3.csv")[['SectionID', 'RoadName', '方向', '路段起點', '路段終點', '行政區']]
#
# section_res = requests.get(f'''http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/SectionShape/AuthorityCode/KHH?$format=json''', headers={"accept": "*/*", "Authorization": "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"})
# section_str = section_res.content.decode('utf-8')
# section_list = json.loads(section_str)
# section_df = pd.json_normalize(section_list)[['SectionID', 'Geometry']]
# section_df['Geometry'] = section_df['Geometry'].str.replace("LINESTRING", "")
# section_df['Geometry'] = section_df['Geometry'].str.replace('(', '[[')
# section_df['Geometry'] = section_df['Geometry'].str.replace(')', ']]')
# section_df['Geometry'] = section_df['Geometry'].str.replace(',', '],[')
# section_df['Geometry'] = section_df['Geometry'].str.replace(' ', ',')
#
# merge_df = pd.merge(intercity_bridge_info_df, section_df, on='SectionID', how='left')
#
# merge_df.rename(columns={"SectionID": "id", "RoadName": "name", '行政區': 'area_name', "方向": "direction", "路段起點": "start_pos", "路段終點": "end_pos", 'Geometry': 'geometry'}, inplace=True)
#
# merge_df['src_time'] = now
# merge_df['update_time'] = now
# merge_df.to_sql('road_section_vd', engine, if_exists='append', index=False, chunksize=500)

'''
id,road_id,road_name,station_o,station_d,o_lat,o_lon,d_lat,d_lon,m_lat,m_lon,remark,SrcUpdateTime,UpdateTime,InfoTime,InfoDate
id
name
direction
start_pos
end_pos
geometry
src_time
update_time
'''
engine.execute(f"DELETE FROM road_section_gvp")
now = datetime.now()
# gvp_df = pd.read_csv(r"gvp/kao_tomtom_road.csv")[['road_id', 'road_name', 'station_o', 'station_d']]
# gvp_df.rename(columns={"road_id": "SectionID"}, inplace=True)

gvp2_df = pd.read_csv(r"gvp/kao_google_road_v4.csv")[['road_id', 'road_name', 'road_direction', 'district']]
gvp2_df.rename(columns={"road_id": "SectionID"}, inplace=True)

section_res = requests.get(f'''http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/GVPSectionShape?$format=json''', headers={"accept": "*/*", "Authorization": "FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF"})
section_str = section_res.content.decode('utf-8')
section_list = json.loads(section_str)
section_df = pd.json_normalize(section_list)[['SectionID', 'Geometry']]
section_df['Geometry'] = section_df['Geometry'].str.replace("LINESTRING", "")
section_df['Geometry'] = section_df['Geometry'].str.replace('(', '[[')
section_df['Geometry'] = section_df['Geometry'].str.replace(')', ']]')
section_df['Geometry'] = section_df['Geometry'].str.replace(' ', '],[')
# merge_df = pd.merge(gvp_df, section_df, on='SectionID', how='inner')
merge_df = pd.merge(gvp2_df, section_df, on='SectionID', how='inner')

merge_df.rename(columns={"SectionID": "id", 'Geometry': 'geometry'}, inplace=True)
merge_df['src_time'] = now
merge_df['update_time'] = now
merge_df.to_sql('road_section_gvp', engine, if_exists='append', index=False, chunksize=500)

