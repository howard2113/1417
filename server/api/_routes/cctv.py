# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
import pandas as pd
import io
from api.models import cctv
import time
import json
import requests
from api.utils.database import db
from api.utils import responses as resp
from api.utils.responses import response_with

cctv_routes = Blueprint("cctv_routes", __name__)


@cctv_routes.route('/info', methods=['GET', 'POST'])
def info():
    cctv_df = pd.read_sql(f"SELECT * FROM cctv_info", con=db.engine)
    res_list = cctv_df.to_dict('records')
    return response_with(resp.SUCCESS_200, value={"data": res_list})


'''
{
    "id": "C000079",
    "name": "自立一路/建國三路口",
    "position": {
        "lat": 22.63792,
        "lng": 120.29647
    },
    "url": "https://cctv6.kctmc.nat.gov.tw/1dd04532/snapshot",
    "locationImage": "https://traffic.tbkc.gov.tw/cctvs/C000079/",
    "org": "KSC",
    "rctvs": [],
    "updateTime": "2021-08-16T10:04:38+08:00"
}


{
    "code": "success",
    "data": [
        {
            "px": 120.30497,
            "py": 22.68577,
            "roadsection": "大中路(高雄)(大中二路/華夏路到大中二路/翠華路)",
            "url": "http://traffic.kctmc.nat.gov.tw/CCTV/cctv_view_atis.jsp?cctv_id=C000001&amp;w=340&amp;h=260",
		"img": 車流圖網址
        },



        {
            "px": 120.29132,
            "py": 22.64191,
            "roadsection": "中華路(中華二路/同盟二路到中華三路/建國三路)",
            "url": "http://traffic.kctmc.nat.gov.tw/CCTV/cctv_view_atis.jsp?cctv_id=C000002&amp;w=340&amp;h=260",
		"img": 車流圖網址
        }
    ]
}

'''

# @cctv_routes.route('/info', methods=['GET', 'POST'])
# def info():
#     # start = request.json['start']
#     # end = request.json['end']
#
#     cctv_static_url = "https://data.kcg.gov.tw/dataset/330df44e-ca1d-4f6c-b790-37507a71b04a/resource/5b986ec0-4f5c-4b8c-9c62-0556caa29f12/download/2k5ws-ha0ly.csv"
#     cctv_dynamic_url = "https://data.kcg.gov.tw/dataset/4d58704d-076f-43c3-a93c-3da068ed6c0e/resource/93d3be35-bf43-4b68-a044-1b3177fddc4e/download/umqnq-hzd4b.csv"
#
#
#     res_cctv_static = requests.get(cctv_static_url).content
#     res_cctv_dynamic = requests.get(cctv_dynamic_url).content
#     df_cctv_static = pd.read_csv(io.StringIO(res_cctv_static.decode('utf-8')))
#     df_cctv_dynamic = pd.read_csv(io.StringIO(res_cctv_dynamic.decode('utf-8')))
#     df_merge = pd.merge(df_cctv_static, df_cctv_dynamic, on='cctvid', how='inner')
#     data = df_merge.to_dict('records')
#
#     return response_with(resp.SUCCESS_200, value={"data": data})
