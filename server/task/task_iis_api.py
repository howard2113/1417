import numpy as np
import time
import collections.abc
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

traffic_section_shape_nfb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/SectionShape/AuthorityCode/NFB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
traffic_live_nfb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/LiveTraffic/AuthorityCode/NFB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
traffic_section_shape_thb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/SectionShape/AuthorityCode/THB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
traffic_live_thb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/LiveTraffic/AuthorityCode/THB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
traffic_section_shape_khh_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/SectionShape/AuthorityCode/KHH?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
traffic_live_khh_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/LiveTraffic/AuthorityCode/KHH?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'

cctv_nfb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/CCTV/AuthorityCode/NFB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
cctv_thb_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/CCTV/AuthorityCode/THB?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'
cctv_khh_url = 'http://tpeits-1.pjm.iisigroup.com/cptapi/Traffic/api/CCTV/AuthorityCode/KHH?$top=30&$format=json&$token=FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF'


def save_api_data2db(url, t_name, next_lv=''):
    res = requests.get(url)
    res_df = pd.DataFrame([{'no': 'no_data'}])
    if res.ok:
        res_list = json.loads(res.content.decode('utf-8'))
        # new_list = []
        # for ele in res_list:
        #     new_dict = {}
        #     for key, chile_ele in ele.items():
        #         if isinstance(chile_ele, dict):
        #             for key2, chile2_ele in chile_ele.items():
        #                 new_dict[key2] = chile2_ele
        #         elif isinstance(chile_ele, list):
        #
        #             for key2, chile2_ele in chile_ele.items():
        #                 new_dict[key2] = chile2_ele
        #         else:
        #             new_dict[key] = chile_ele
        #     new_list.append(new_dict)
        # if len(new_list):
        #     res_df = pd.DataFrame(new_list)

        if len(res_list):
            res_df = pd.DataFrame(res_list)
            if next_lv in res_df:
                res_df[next_lv] = res_df[next_lv].astype('string')
    res_df.to_sql(t_name, engine, if_exists='replace', index=False, chunksize=500, )

save_api_data2db(traffic_section_shape_nfb_url, 'traffic_section_shape_nfb')
save_api_data2db(traffic_live_nfb_url, 'traffic_live_nfb', 'DataSources')
save_api_data2db(traffic_section_shape_thb_url, 'traffic_section_shape_thb')
save_api_data2db(traffic_live_thb_url, 'traffic_live_thb', 'DataSources')
save_api_data2db(traffic_section_shape_khh_url, 'traffic_section_shape_khh')
save_api_data2db(traffic_live_khh_url, 'traffic_live_khh', 'DataSources')

save_api_data2db(cctv_nfb_url, 'cctv_nfb')
save_api_data2db(cctv_thb_url, 'cctv_thb')
save_api_data2db(cctv_khh_url, 'cctv_khh', 'LookingViews')
