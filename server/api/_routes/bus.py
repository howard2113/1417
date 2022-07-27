# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
import pandas as pd
from api.models import bus
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

bus_routes = Blueprint("bus_routes", __name__)


@bus_routes.route('/info', methods=['GET', 'POST'])
def info():
    '''
    [{
      "id(接駁車路線id)" : "string",
      "name(接駁車路線名稱)" : "string",
      "count(運載次數)" : "int",
      "people(運載人數)" : "int",
      "src_time(資料時間)" : "datetime",
    }]
    '''
    bus_dynamic_df = pd.read_sql("SELECT * FROM bus_dynamic;", con=db.engine)
    bus_dynamic_dict = bus_dynamic_df.to_dict('records')

    return response_with(resp.SUCCESS_200, value={"data": bus_dynamic_dict}, )


