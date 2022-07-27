# -*- coding: utf-8 -*-
import time
import numpy as np
import pandas as pd
from datetime import datetime
from flask import Blueprint
from flask import request
import requests
from api.models import parking
from api.utils import responses as resp
from api.utils.database import db, mysql2csv, hour_map
from api.utils.responses import response_with

parking_routes = Blueprint("parking_routes", __name__)

sp_p_map = {'停2572': {'name': '夢時代購物中心附屬停車場', 'volumn': 2630},
            '停4525': {'name': '大東文化藝術中心地下停車場', 'volumn': 251},
            '停3893': {'name': '高雄捷運R24南岡山站第一停車場', 'volumn': 207},
            '停4308': {'name': '高鐵左營站停車場', 'volumn': 780},
            '停4679': {'name': '衛武營國家藝術文化中心地下停車場', 'volumn': 716},
            'AD04': {'name': '文化中心停車場', 'volumn': 830},
            '停4370': {'name': '前金立體停車場', 'volumn': 648},
            '停4026': {'name': '草衙道地下停車場', 'volumn': 967},
            'car5': {'name': '高雄國際機場停車場', 'volumn': 1051},
            '停3364': {'name': '高雄捷運R22青埔站轉乘停車場', 'volumn': 97},
            '448a': {'name': '捷運都會公園站轉乘停車場', 'volumn': 287},
            'AA23': {'name': '美術館立體停車場', 'volumn': 333},
            '816': {'name': '國泰青年停車場', 'volumn': 514},
            'car10': {'name': '捷運大寮站轉乘停車場', 'volumn': 88}}

@parking_routes.route('/static', methods=['GET', 'POST'])
def static():
    '''
    [{
      "name(停車場名稱)" : "string",
      "areaname(行政區域)" : "string",
      "volumn(總格位)" : "int",
      "lat(緯度)" : "float/decimal",
      "lng(經度)" : "float/decimal",
    }]
    '''
    parking_static_df = pd.read_sql("SELECT * FROM parking_outer_static;", con=db.engine)
    parking_static_df['volume'] = parking_static_df['volumn']
    parking_static_df = parking_static_df[parking_static_df['volumn'] > 0]
    parking_static_dict = parking_static_df.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": parking_static_dict})


@parking_routes.route('/remaining', methods=['GET', 'POST'])
def remaining():
    now = datetime.now()
    if now.minute <= 5:
        now.replace(hour=now.hour - 1)
    # header_list = ['id', 'name', 'volume', hour_map[now.hour], 'src_time']
    # parking_dynamic_df = mysql2csv(f"SELECT {','.join(header_list)} FROM parking_outer_left_space_dynamic", header_list, db.engine)
    parking_dynamic_df = pd.read_sql(f"SELECT id,name,v_type,volumn,leftspace,src_time,update_time,{hour_map[now.hour]} FROM parking_outer_left_space_dynamic;", con=db.engine)
    parking_dynamic_df['volume'] = parking_dynamic_df['volumn']
    max_src_time = parking_dynamic_df['src_time'].max().strftime('%Y/%m/%d %H:%M:%S')
    parking_dynamic_dict = parking_dynamic_df.to_dict('records')
    '''
    "data": [
            {
                "leftspace": 0,
                "name": "三鳳中街機車",
                "p_id": "093",
                "src_time": "2021-08-20 17:20:12",
                "total_space": 136
            },...
            ...
        ]
    '''
    return response_with(resp.SUCCESS_200, value={"data": parking_dynamic_dict, 'max_src_time': max_src_time})


@parking_routes.route('/remaining_by_id/<id>', methods=['GET', 'POST'])
def remaining_by_id(id):
    now = datetime.now()
    if now.minute <= 5:
        now.replace(hour=now.hour - 1)
    parking_dynamic_df = pd.read_sql(f"SELECT id,name,v_type,volumn,leftspace,src_time,update_time,{hour_map[now.hour]} FROM parking_outer_left_space_dynamic WHERE id='{id}';", con=db.engine)
    parking_dynamic_df['volume'] = parking_dynamic_df['volumn']
    max_src_time = parking_dynamic_df['src_time'].max().strftime('%Y/%m/%d %H:%M:%S')
    parking_dynamic_dict = parking_dynamic_df.to_dict('records')[0]
    '''
    "data": {
                "leftspace": 0,
                "name": "三鳳中街機車",
                "p_id": "093",
                "src_time": "2021-08-20 17:20:12",
                "total_space": 136
            },...
            ...
    '''
    return response_with(resp.SUCCESS_200, value={"data": parking_dynamic_dict, 'max_src_time': max_src_time})


@parking_routes.route('/rate', methods=['GET', 'POST'])
def rate():
    now = datetime.now()
    p_ids = request.get_json()['p_ids']
    if now.minute <= 5:
        now.replace(hour=now.hour - 1)
    parking_dynamic_df = pd.read_sql(f"SELECT id,name,v_type,volumn,leftspace,src_time,update_time,{hour_map[now.hour]} FROM parking_outer_left_space_dynamic;", con=db.engine)
    parking_dynamic_df = parking_dynamic_df[parking_dynamic_df.id.isin(p_ids)]
    parking_dynamic_left_df = parking_dynamic_df[parking_dynamic_df['leftspace'] >= 0]
    if len(parking_dynamic_left_df.index) > 0:
        volume_sum = int(parking_dynamic_df['volumn'].sum())
        left_sum = int(parking_dynamic_left_df['leftspace'].sum())
        max_src_time = parking_dynamic_left_df['src_time'].max().strftime('%Y/%m/%d %H:%M:%S')
    elif len(parking_dynamic_df.index) > 0:
        volume_sum = int(parking_dynamic_df['volumn'].sum())
        left_sum = volume_sum
        max_src_time = 0
    else:
        volume_sum = 0
        left_sum = 0
        max_src_time = 0
    rate_num = 0
    if volume_sum > 0:
        rate_num = round((1 - left_sum / volume_sum) * 100)
    if rate_num < 0:
        rate_num = -1

    '''
    {
        "code": "success",
        "data": {
            "left_sum": 4,
            "rate": 3.0,
            "volume_sum": 123
        },
        "max_src_time": "2021/10/09 10:40:02"
    }
    '''
    return response_with(resp.SUCCESS_200, value={"data": {'rate': rate_num, 'left_sum': left_sum, 'volume_sum': volume_sum}, 'max_src_time': max_src_time})


@parking_routes.route('/rates', methods=['GET', 'POST'])
def rates():
    now = datetime.now()
    p_ids = request.get_json()['p_ids']
    if now.minute <= 5:
        now.replace(hour=now.hour - 1)
    parking_dynamic_df = pd.read_sql(f"SELECT id,name,v_type,volumn,leftspace,src_time,update_time,{hour_map[now.hour]} FROM parking_outer_left_space_dynamic;", con=db.engine)
    parking_dynamic_df = parking_dynamic_df[parking_dynamic_df.id.isin(p_ids)]
    max_src_time = parking_dynamic_df['src_time'].max().strftime('%Y/%m/%d %H:%M:%S')
    data = {}




    for p_id in p_ids:
        row_dict = parking_dynamic_df[parking_dynamic_df['id'] == p_id].to_dict('records')
        if len(row_dict) <= 0:
            data[sp_p_map[p_id]['name']] = {'rate': -1, 'leftspace': -1}
        else:
            rate = -1
            if row_dict[0]['volumn'] > 0 and row_dict[0]['leftspace'] >= 0:
                rate = round((1 - row_dict[0]['leftspace'] / row_dict[0]['volumn']) * 100)

            data[row_dict[0]['name']] = {'rate': rate, 'leftspace': row_dict[0]['leftspace']}

    return response_with(resp.SUCCESS_200, value={"data": data, 'max_src_time': max_src_time})


@parking_routes.route('/info24h', methods=['GET', 'POST'])
def info24h():
    # parking_id_list = request.json['parking']
    # start = request.json['start']
    # end = request.json['end']
    '''
    {
     "(停車場名稱)" : [24小時資料排序0-23],
    (下面是舉例)
     "公園停車場" : [0,1,2,3,5,5,5,5,5...]
     =============================================
    name.update_time.dt.strftime('%Y/%m/%d %H:%M:%S')
    '''

    p_ids = request.get_json()['p_ids']
    now = datetime.now()
    pd_df = pd.read_sql('SELECT * FROM parking_outer_left_space_dynamic', db.engine)
    if len(p_ids) > 0:
        pd_df = pd_df[pd_df.id.isin(p_ids)]

    pd_df.replace(-1, np.nan, inplace=True)
    for hr in hour_map:
        pd_df[hr] = round((1 - pd_df[hr] / pd_df['volumn']) * 100)
    pd_df.fillna('', inplace=True)
    name_df = pd_df[['name']]
    src_time_df = pd_df['src_time']

    max_src_time = src_time_df.max().strftime('%Y/%m/%d %H:%M:%S')
    data = []
    for idx, p_name in name_df.iterrows():
        hr24_list = pd_df[hour_map].loc[[idx]].values.flatten().tolist()
        # hr24_list = hr24_df.loc[[idx]].values[0]
        if now.hour < 23:
            # hr24_list[now.hour + 1:] = [-1] * (23 - now.hour)
            hr24_list[now.hour + 1:] = [''] * (23 - now.hour)
        data.append({p_name['name']: hr24_list})

    return response_with(resp.SUCCESS_200, value={"data": data, 'max_src_time': max_src_time})
