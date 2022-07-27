# -*- coding: utf-8 -*-
import requests
import io
import pandas as pd
from flask import Blueprint
from flask import request
import json
from api.models.notify import NotifyHistory, NotifyHistorySchema
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

weather_routes = Blueprint("weather_routes", __name__)


@weather_routes.route('/info', methods=['GET', 'POST'])
def static():
    weather_info_url = "https://opendata.cwb.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWB-C81EDBC1-7B60-4465-AD9C-5C35D1DC3B6F&format=JSON&locationName=高雄市"

    weather_info = requests.get(weather_info_url).content
    # weather_info_dict = pd.read_csv(io.StringIO(weather_info.decode('utf-8'))).to_dict('records')
    weather_info_dict = json.loads(weather_info)
    return response_with(resp.SUCCESS_200, value={"data": weather_info_dict})
