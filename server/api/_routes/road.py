# -*- coding: utf-8 -*-
import json

import pandas as pd
import random
from datetime import datetime
from flask import Blueprint
from flask import request
from api.models import road_speed, road_flow
from api.utils import responses as resp
from api.utils.database import db, hour_map
from api.utils.responses import response_with

road_routes = Blueprint("road_routes", __name__)


def collect_time_between_hours(now_time):
    hour_list = pd.date_range(now_time.strftime('%Y-%m-%d'), periods=24, freq='1H')
    for hour, dt in enumerate(hour_list):
        if hour_list[hour - 1] <= now_time < dt:
            return hour - 1


@road_routes.route('/vd_static', methods=['GET', 'POST'])
def vd_static():
    '''
    [{
      "id(路段id)" : "string",
      "name(路段名稱)" : "string",
      "areaname(行政區)" : "string",#暫時空值
      "lat(緯度)" : "float/decimal",
      "lng(經度)" : "float/decimal",
    }]
       id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    areaname = db.Column(db.String(10))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    '''
    road_static_vd_df = pd.read_sql("SELECT * FROM road_static_vd;", con=db.engine)
    road_static_vd_dict = road_static_vd_df.to_dict('records')

    return response_with(resp.SUCCESS_200, value={"data": road_static_vd_dict})


@road_routes.route('/vd_section', methods=['GET', 'POST'])
def vd_section():
    road_static_vd_df = pd.read_sql("SELECT * FROM road_section_vd;", con=db.engine)
    no_repeat_gvp_section = road_static_vd_df[road_static_vd_df['id'].isin(
        ['L_6192540200020E', 'L_6192540200070E', 'L_6192540600020E', 'L_6192540600070E', 'L_6193130000030E', 'L_6193130400030E',
         'L_6193150000050E', 'L_6193150400050E', 'L_6193160000030E', 'L_6193160000050E', 'L_6193160400030E', 'L_6193160400050E',
         'L_6193160400070E', 'L_6193600200050E', 'L_6193600600040E', 'L_6193620300030E', 'L_6193620300050E', 'L_6193620700030E',
         'L_6193620700050E', 'L_6194200200020E', 'L_6194200200040E', 'L_6194200600020E', 'L_6194200600040E', 'L_6198330000050E',
         'L_6198330000080E', 'L_6198330400050E', 'L_6198330400080E', 'L_6198340000060E', 'L_6198340400060E', 'L_6207700100040E',

         'L_6203090000020E', 'L_6203090000060E', 'L_6203090400020E', 'L_6203090400060E', 'L_6207140100020E', 'L_6207140500020E',
         'L_6208600100060E', 'L_6208600100120E', 'L_6208600400010E', 'L_6208600400070E'
         ])]

    road_static_vd_df.drop(no_repeat_gvp_section.index, inplace=True)
    # road_static_vd_df = road_static_vd_df[road_static_vd_df['geometry'].str.contains('None')]
    road_static_vd_df = road_static_vd_df.dropna()
    road_static_vd_dict = road_static_vd_df.to_dict('records')
    for road_static_vd in road_static_vd_dict:
        if not road_static_vd['geometry'] is None:
            road_static_vd['geometry'] = json.loads(road_static_vd['geometry'])

    return response_with(resp.SUCCESS_200, value={"data": road_static_vd_dict})


@road_routes.route('/gvp_section', methods=['GET', 'POST'])
def gvp_section():
    '''
    [{
      "id(路段id)" : "string",
      "name(路段名稱)" : "string",
      "areaname(行政區)" : "string",#暫時空值
      "lat(緯度)" : "float/decimal",
      "lng(經度)" : "float/decimal",
    }]
       id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(50))
    areaname = db.Column(db.String(10))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    '''
    road_static_gvp_df = pd.read_sql("SELECT * FROM road_section_gvp;", con=db.engine)
    road_static_gvp_df = road_static_gvp_df.dropna()
    road_static_gvp_dict = road_static_gvp_df.to_dict('records')
    for road_static_gvp in road_static_gvp_dict:
        road_static_gvp['geometry'] = json.loads(road_static_gvp['geometry']);

    return response_with(resp.SUCCESS_200, value={"data": road_static_gvp_dict})


@road_routes.route('/speed_24hr', methods=['GET', 'POST'])
def speed_24hr():
    '''
    路段分時行駛速率趨勢
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "speedHR24": [11, 11, 11, -1, -1, ...], // 該路段今日0時~23時速率，無資料為-1
          "updatetime": "2021/08/19 19:30", // 最後更新時間
        },
      ]
    }
    '''
    now = datetime.now()
    road_dynamic_speed_df = pd.read_sql("SELECT * FROM road_dynamic_speed;", con=db.engine)
    update_time = road_dynamic_speed_df['src_time'].max()
    road_dynamic_speed_df['now'] = now
    road_dynamic_speed_df['delta_sec'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.seconds
    road_dynamic_speed_df['delta_day'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.days

    # road_dynamic_speed_df[~road_dynamic_speed_df['l_id'].str.contains('kao')]['l_id'] = 'L_'
    road_dynamic_speed_df.loc[(~road_dynamic_speed_df['id'].str.contains('kao')), 'l_id'] = 'L_'+road_dynamic_speed_df[~road_dynamic_speed_df['l_id'].str.contains('kao')]['l_id']
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_day'] == 0]
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_sec'] < 1800]
    hr24_df = road_dynamic_speed_df[hour_map]
    name = road_dynamic_speed_df[['l_id', 'name', 'dev', 'area_name', 'src_time']]

    data_list = []
    for idx, row in name.iterrows():
        hr24_list = hr24_df.loc[[idx]].values.flatten().tolist()
        # if row['dev'] == 1:
        #     hr24_list[now.hour] = -1.0
        # if now.hour < 23:
        #     hr24_list[now.hour + 1:] = [-1] * (23 - now.hour)
        data_list.append({'l_id': row['l_id'], 'dev': row['dev'], 'area_name': row['area_name'], 'name': row['name'], 'update_time': row['src_time'], 'speed_hr24': hr24_list})

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})


@road_routes.route('/flow_24hr', methods=['GET', 'POST'])
def flow_24hr():
    '''
    路段分時車輛數趨勢
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "pcuHR24": [192.7, 314.8, 551.2, -1, -1, ...], // 該路段今日0時~23時pcu，無資料為-1
          "updatetime": "2021/08/19 19:30", // 最後更新時間
        },
      ]
    }
    '''
    now = datetime.now()
    road_dynamic_flow_df = pd.read_sql("SELECT * FROM road_dynamic_flow;", con=db.engine)

    update_time = road_dynamic_flow_df['src_time'].max()
    road_dynamic_flow_df['now'] = now
    road_dynamic_flow_df['delta_sec'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.seconds
    road_dynamic_flow_df['delta_day'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.days
    road_dynamic_flow_df['l_id'] = 'L_' + road_dynamic_flow_df['l_id']
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_day'] == 0]
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_sec'] < 1800]
    hr24_df = road_dynamic_flow_df[hour_map]
    name = road_dynamic_flow_df[['l_id', 'dev', 'name', 'area_name', 'src_time']]

    data_list = []
    for idx, row in name.iterrows():
        hr24_list = hr24_df.loc[[idx]].values.flatten().tolist()
        # if now.hour < 23:
        #     hr24_list[now.hour + 1:] = [-1] * (23 - now.hour)
        data_list.append({'l_id': row['l_id'], 'dev': row['dev'], 'area_name': row['area_name'], 'name': row['name'], 'update_time': row['src_time'], 'pcu_hr24': hr24_list})

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})


@road_routes.route('/flow_rank', methods=['GET', 'POST'])
def flow_rank():
    '''
    在線車輛數排名(依照 pcu正序 )
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "pcu": 192.7, // 路段pcu
        },
        {
          "areaname": "梓官區",
          "name": "成功一路(三多四路~五福三路)",
          "pcu": 154.3,
        },
      ]
    }
    '''
    now = datetime.now()
    road_dynamic_flow_df = pd.read_sql("SELECT * FROM road_dynamic_flow;", con=db.engine)
    update_time = road_dynamic_flow_df['src_time'].max()
    road_dynamic_flow_df = road_dynamic_flow_df[['l_id', 'dev', 'name', 'area_name', 'pcu', 'src_time']]
    road_dynamic_flow_df['now'] = now
    road_dynamic_flow_df['delta_sec'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.seconds
    road_dynamic_flow_df['delta_day'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.days
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_day'] == 0]
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_sec'] < 1800]

    road_dynamic_flow_df.sort_values('pcu', inplace=True, ascending=False)
    data_list = road_dynamic_flow_df.to_dict('records')

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})


@road_routes.route('/speed_rank', methods=['GET', 'POST'])
def speed_rank():
    '''
    壅塞路段行駛速率(依照 tti倒序 )
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "speed": 43, // 時速
          "tti": 0.48, // tti
        },
        {
          "areaname": "梓官區",
          "name": "成功一路(三多四路~五福三路)",
          "speed": 37,
          "tti": 0.52,
        },
      ]
    }
    '''

    now = datetime.now()
    road_dynamic_speed_df = pd.read_sql("SELECT * FROM road_dynamic_speed;", con=db.engine)
    road_dynamic_speed_df = road_dynamic_speed_df[['l_id', 'dev', 'name', 'area_name', 'tti', 'speed', 'src_time']]
    update_time = road_dynamic_speed_df['src_time'].max()
    road_dynamic_speed_df['now'] = now
    road_dynamic_speed_df['delta_sec'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.seconds
    road_dynamic_speed_df['delta_day'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.days
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_day'] == 0]
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_sec'] < 1800]

    road_dynamic_speed_df.sort_values('tti', inplace=True, ascending=True)
    data_list = road_dynamic_speed_df.to_dict('records')

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})


@road_routes.route('/speed_by_id', methods=['GET', 'POST'])
def speed_by_id():
    '''
    壅塞路段行駛速率(依照 tti倒序 )
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "speed": 43, // 時速
          "tti": 0.48, // tti
        },
        {
          "areaname": "梓官區",
          "name": "成功一路(三多四路~五福三路)",
          "speed": 37,
          "tti": 0.52,
        },
      ]
    }
    '''

    # l_ids = request.args.getlist('l_ids')
    l_ids = request.get_json()['l_ids']
    now = datetime.now()
    road_dynamic_speed_df = pd.read_sql(f"SELECT * FROM road_dynamic_speed", con=db.engine)
    road_dynamic_speed_df = road_dynamic_speed_df[['l_id', 'dev', 'name', 'area_name', 'tti', 'speed', 'src_time']]
    if len(l_ids) > 0:
        road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df.l_id.isin(l_ids)]
    road_dynamic_speed_df.sort_values('tti', inplace=True, ascending=True)
    road_dynamic_speed_df['now'] = now
    road_dynamic_speed_df['delta_sec'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.seconds
    road_dynamic_speed_df['delta_day'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.days
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_day'] == 0]
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_sec'] < 1800]
    data_list = road_dynamic_speed_df.to_dict('records')
    update_time = road_dynamic_speed_df['src_time'].max()

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})


@road_routes.route('/flow_by_id', methods=['GET', 'POST'])
def flow_by_id():
    '''
    各路段流量
    response
{
  "code": "success",
  "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
  "data": [
    ...{
      "areaname": "三民區", // 行政區名稱
      "name": "中華三路(五福三路~中正四路)", // 路段名稱
      "pcu": 147.4, // pcu
      "updatetime": "2021/08/19 19:30", // 最後更新時間
    },
  ]
}
    '''
    # l_ids = request.args.getlist('l_ids')
    l_ids = request.get_json()['l_ids']
    now = datetime.now()
    road_dynamic_flow_df = pd.read_sql(f"SELECT * FROM road_dynamic_flow", con=db.engine)
    road_dynamic_flow_df = road_dynamic_flow_df[['l_id', 'dev', 'name', 'area_name', 'pcu', 'src_time']]
    if len(l_ids) > 0:
        road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df.l_id.isin(l_ids)]
    road_dynamic_flow_df['now'] = now
    road_dynamic_flow_df['delta_sec'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.seconds
    road_dynamic_flow_df['delta_day'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.days
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_day'] == 0]
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_sec'] < 1800]
    data_list = road_dynamic_flow_df.to_dict('records')
    update_time = road_dynamic_flow_df['src_time'].max()

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})



@road_routes.route('/flow_24hr_by_id', methods=['GET', 'POST'])
def flow_24hr_by_id():
    '''
    路段分時車輛數趨勢
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "pcuHR24": [192.7, 314.8, 551.2, -1, -1, ...], // 該路段今日0時~23時pcu，無資料為-1
          "updatetime": "2021/08/19 19:30", // 最後更新時間
        },
      ]
    }
    '''
    # l_ids = request.args.getlist('l_ids')
    l_ids = request.get_json()['l_ids']
    now = datetime.now()
    road_dynamic_flow_df = pd.read_sql("SELECT * FROM road_dynamic_flow;", con=db.engine)



    update_time = road_dynamic_flow_df['src_time'].max()
    road_dynamic_flow_df['now'] = now
    road_dynamic_flow_df['delta_sec'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.seconds
    road_dynamic_flow_df['delta_day'] = (road_dynamic_flow_df['now'] - road_dynamic_flow_df['src_time']).dt.days

    if len(l_ids) > 0:
        road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df.l_id.isin(l_ids)]
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_day'] == 0]
    road_dynamic_flow_df = road_dynamic_flow_df[road_dynamic_flow_df['delta_sec'] < 1800]
    hr24_df = road_dynamic_flow_df[hour_map]
    name = road_dynamic_flow_df[['l_id', 'dev', 'name', 'area_name', 'src_time']]

    data_list = []
    for idx, row in name.iterrows():
        hr24_list = hr24_df.loc[[idx]].values.flatten().tolist()
        # if now.hour < 23:
        #     hr24_list[now.hour + 1:] = [-1] * (23 - now.hour)
        data_list.append({'l_id': row['l_id'], 'dev': row['dev'], 'area_name': row['area_name'], 'name': row['name'], 'update_time': row['src_time'], 'pcu_hr24': hr24_list})

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})



@road_routes.route('/speed_24hr_by_id', methods=['GET', 'POST'])
def speed_24hr_by_id():
    '''
    路段分時行駛速率趨勢
    response
    {
      "code": "success",
      "updatetime": "2021/08/19 19:30", // 最新一筆最後更新時間
      "data": [
        ...{
          "areaname": "三民區", // 行政區名稱
          "name": "中華三路(五福三路~中正四路)", // 路段名稱
          "speedHR24": [11, 11, 11, -1, -1, ...], // 該路段今日0時~23時速率，無資料為-1
          "updatetime": "2021/08/19 19:30", // 最後更新時間
        },
      ]
    }
    '''
    # l_ids = request.args.getlist('l_ids')
    l_ids = request.get_json()['l_ids']
    now = datetime.now()
    road_dynamic_speed_df = pd.read_sql("SELECT * FROM road_dynamic_speed;", con=db.engine)


    update_time = road_dynamic_speed_df['src_time'].max()
    road_dynamic_speed_df['now'] = now
    road_dynamic_speed_df['delta_sec'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.seconds
    road_dynamic_speed_df['delta_day'] = (road_dynamic_speed_df['now'] - road_dynamic_speed_df['src_time']).dt.days


    if len(l_ids) > 0:
        road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df.l_id.isin(l_ids)]
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_day'] == 0]
    road_dynamic_speed_df = road_dynamic_speed_df[road_dynamic_speed_df['delta_sec'] < 1800]
    hr24_df = road_dynamic_speed_df[hour_map]
    name = road_dynamic_speed_df[['l_id', 'name', 'dev', 'area_name', 'src_time']]

    data_list = []
    for idx, row in name.iterrows():
        hr24_list = hr24_df.loc[[idx]].values.flatten().tolist()
        # if row['dev'] == 1:
        #     hr24_list[now.hour] = -1.0
        # if now.hour < 23:
        #     hr24_list[now.hour + 1:] = [-1] * (23 - now.hour)
        data_list.append({'l_id': row['l_id'], 'dev': row['dev'], 'area_name': row['area_name'], 'name': row['name'], 'update_time': row['src_time'], 'speed_hr24': hr24_list})

    return response_with(resp.SUCCESS_200, value={"data": data_list, 'update_time': update_time})