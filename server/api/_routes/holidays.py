# -*- coding: utf-8 -*-
import datetime

from flask import Blueprint

from api.models.holidays import Holiday, HolidaySchema
from api.utils import responses as resp
from api.utils.responses import response_with
# from api.utils.statics import HolidayCollect

holiday_routes = Blueprint("holiday_routes", __name__)
FreeFlowDict = {}

@holiday_routes.route('/', methods=['GET'])
def get_holiday():
    
    fetched = Holiday.query.all()
    holiday_schema = HolidaySchema(many=True, only=['Date_datetime', 'isWorkday'])
    holidays = holiday_schema.dump(fetched)

    # if len(HolidayCollect) == 0:
    #     fetched = Holiday.query.all()
    #     holiday_schema = HolidaySchema(many=True, only=['Date_datetime', 'isWorkday'])
    #     holidays = holiday_schema.dump(fetched)
    #     for rec in holidays:
    #         recTime = datetime.datetime.strptime(rec['Date_datetime'], '%Y-%m-%d %H:%M:%S')
    #         isWorkday = rec['isWorkday']
    #         HolidayCollect[recTime] = int(isWorkday)


    return response_with(resp.SUCCESS_200, value={"holidays": holidays},)

