# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
import pandas as pd
import time
from datetime import datetime, timedelta
from api.models import people
from api.utils import responses as resp
from api.utils.database import db, mysql2csv
from api.utils.responses import response_with

people_routes = Blueprint("people_routes", __name__)
city_map = {'A': '臺北市', 'B': '臺中市', 'C': '基隆市', 'D': '臺南市', 'E': '高雄市', 'F': '新北市', 'G': '宜蘭縣', 'H': '桃園縣', 'J': '新竹縣', 'K': '苗栗縣', 'M': '南投縣', 'N': '彰化縣', 'P': '雲林縣', 'Q': '嘉義縣', 'R': '臺南縣', 'S': '高雄縣', 'T': '屏東縣', 'U': '花蓮縣', 'V': '臺東縣', 'X': '澎湖縣', 'W': '金門縣', 'Z': '連江縣', 'I': '嘉義市', 'O': '新竹市'}
_hour_map = ['_h0', '_h1', '_h2', '_h3', '_h4', '_h5', '_h6', '_h7', '_h8', '_h9', '_h10', '_h11', '_h12', '_h13', '_h14', '_h15', '_h16', '_h17', '_h18', '_h19', '_h20', '_h21', '_h22', '_h23']
hour_map = ['h0', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'h7', 'h8', 'h9', 'h10', 'h11', 'h12', 'h13', 'h14', 'h15', 'h16', 'h17', 'h18', 'h19', 'h20', 'h21', 'h22', 'h23']


@people_routes.route('/count', methods=['GET', 'POST'])
def count():
    start = request.json['start']
    end = request.json['end']

    people_dynamic_df = pd.read_sql(f"SELECT * FROM people_dynamic where updatetime >= '{start}' and updatetime <= '{end}';", con=db.engine)
    people_dynamic_group = people_dynamic_df.groupby('name')
    data_list = []
    for name, group in people_dynamic_group:
        data = {'name': name, 'data': {}}
        updatetime_list = group['updatetime'].tolist()
        count_list = group['count'].tolist()
        for idx, updatetime in enumerate(updatetime_list):
            updatetime_str = updatetime.strftime('%Y-%m-%d %H:%M:%S')
            data['data'][updatetime_str] = count_list[idx]
        data_list.append(data)

    return response_with(resp.SUCCESS_200, value={"data": data_list})


@people_routes.route('/mrt_count', methods=['GET', 'POST'])
def mrt_count():
    mrt_count_df = pd.read_sql(f"SELECT * FROM mrt_count", con=db.engine)
    mrt_count_df.drop(['train_type', 'enter_rank', 'exit_rank'], inplace=True, axis=1)
    max_scr_time = mrt_count_df['src_time'].max()

    data_list = mrt_count_df.to_dict('records')
    data_list.sort(key=lambda s: s['enter'], reverse=True)

    return response_with(resp.SUCCESS_200, value={"data": data_list, "max_scr_time": max_scr_time})


@people_routes.route('/cvp_rt_grid_count', methods=['GET', 'POST'])
def cvp_rt_grid_count():
    # cvp_rt_grid_df = pd.read_sql(f"SELECT * FROM cvp_rt_grid_data", con=db.engine)
    # header_list = ['gid', 'population', 'lat', 'lon', 'data_time']
    # cvp_rt_grid_df = mysql2csv(f"SELECT {','.join(header_list)} FROM cvp_rt_grid_data", header_list, db.engine)
    now = datetime.now()
    start_time_str = now.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y/%m/%d %H:%M:%S')
    cvp_rt_grid_df = pd.read_sql(f"SELECT * FROM cvp_rt_grid_data where '{start_time_str}' <= src_time;", con=db.engine)
    start_t = time.time()
    data_list = cvp_rt_grid_df.to_dict('records')
    print(time.time() - start_t)
    return response_with(resp.SUCCESS_200, value={"data": data_list})


@people_routes.route('/cvp_twrt_count', methods=['GET', 'POST'])
def cvp_twrt_count():
    cvp_twrt_df = pd.read_sql(f"SELECT * FROM cvp_twrt_data", con=db.engine)
    data = cvp_twrt_df.to_dict('records')[0]
    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_twrt_city_count', methods=['GET', 'POST'])
def cvp_twrt_city_count():
    cvp_twrt_city_df = pd.read_sql(f"SELECT * FROM cvp_twrt_city_data", con=db.engine)
    for code, name in city_map.items():
        cvp_twrt_city_df.rename(columns={code: name}, inplace=True)
    data = cvp_twrt_city_df.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_twrt_age_count', methods=['GET', 'POST'])
def cvp_twrt_age_count():
    cvp_twrt_age_df = pd.read_sql(f"SELECT * FROM cvp_twrt_age_data", con=db.engine)
    for code, name in city_map.items():
        cvp_twrt_age_df.rename(columns={code: name}, inplace=True)
    data = cvp_twrt_age_df.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_popu_total', methods=['GET', 'POST'])
def cvp_popu_total():
    now = datetime.now()
    cvp_popu_df = pd.read_sql(f"SELECT name, count, src_time FROM cvp_popu_data", con=db.engine)
    # cvp_popu_df.rename(columns={f"h{now.hour}": "count"}, inplace=True)
    data = cvp_popu_df.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_popu_realtime', methods=['GET', 'POST'])
def cvp_popu_realtime():
    sub_grid_count = pd.read_sql(f"SELECT name, count, src_time FROM sub_grid_count WHERE name='亞灣區活動遊客分析範圍'", con=db.engine)
    data = sub_grid_count.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_popu_24hr', methods=['GET', 'POST'])
def cvp_popu_24hr():
    data = []
    cvp_popu_df = pd.read_sql(f"SELECT * FROM cvp_popu_data", con=db.engine)
    now = datetime.now()
    for i, hour_col in enumerate(hour_map):
        if hour_col == 'h0':
            cvp_popu_df[f'_h0'] = cvp_popu_df['h0']-cvp_popu_df['h23']
        else:
            cvp_popu_df[f'_{hour_col}'] = cvp_popu_df[f'h{i}'] - cvp_popu_df[f'h{i - 1}']
            cvp_popu_df.loc[(cvp_popu_df[f'_{hour_col}'] < 0), f'_{hour_col}'] = 0



    cvp_popu_df[f'_h{now.hour+1}'] = 0

        # elif now.hour >= i:
        #     cvp_popu_df[f'_{hour_col}'] = cvp_popu_df[f'h{i}'] - cvp_popu_df[f'h{i - 1}']
            # cvp_popu_df.loc[(cvp_popu_df[f'_{hour_col}'] < 0, f'_{hour_col}')] = 0
        # elif now.hour < i:
        #     cvp_popu_df[f'_{hour_col}'] = 0

        # if i < 8:
        #     cvp_popu_df[f'_{hour_col}'] = 0
        #     cvp_popu_df[f'{hour_col}'] = 0
        # elif hour_col == 'h8':
        #     cvp_popu_df[f'_h8'] = cvp_popu_df['h8']
        # elif now.hour >= i:
        #     cvp_popu_df[f'_{hour_col}'] = cvp_popu_df[f'h{i}'] - cvp_popu_df[f'h{i - 1}']
        #     cvp_popu_df.loc[(cvp_popu_df[f'_{hour_col}'] < 0, f'_{hour_col}')] = 0
        # elif now.hour < i:
        #     cvp_popu_df[f'_{hour_col}'] = 0
        #     cvp_popu_df[f'{hour_col}'] = 0

    hr24_df = cvp_popu_df[_hour_map]
    hr24_list = hr24_df.values.tolist()

    total_hr24_df = cvp_popu_df[hour_map]
    total_hr24_list = total_hr24_df.values.tolist()
    for idx, cvp_popu in cvp_popu_df.iterrows():
        data.append({'name': cvp_popu['name'], 'total_count_24h': total_hr24_list[idx], 'count_24h': hr24_list[idx], 'src_time': cvp_popu['src_time']})

    return response_with(resp.SUCCESS_200, value={"data": data})


@people_routes.route('/cvp_area_rank', methods=['GET', 'POST'])
def cvp_area_rank():
    sub_grid_count = pd.read_sql(f"SELECT name, count, src_time FROM sub_grid_count", con=db.engine)
    sub_grid_count = sub_grid_count[sub_grid_count['name'] != '亞灣區活動遊客分析範圍']
    data_list = sub_grid_count.to_dict('records')
    data_list.sort(key=lambda s: s['count'], reverse=True)
    return response_with(resp.SUCCESS_200, value={"data": data_list})
