# -*- coding: utf-8 -*-
import requests
from flask import Blueprint
import json
import pandas as pd
from flask import request
from api.models.ui import Ui_record
from api.utils import responses as resp
from api.utils.responses import response_with
from api.utils.database import db, mysql2csv
from flask_jwt_extended import (jwt_required, get_jwt_identity)

ui_record_routes = Blueprint("ui_record_routes", __name__)

@ui_record_routes.route('/get_ui_record', methods=['GET'])
@jwt_required
def get_ui_record():
    user_id = get_jwt_identity()
    ui_record_df = pd.read_sql(f"SELECT * FROM ui_record WHERE user_id={user_id}", con=db.engine)[['page_configs', 'update_time']]
    aa=ui_record_df.to_dict('records')[0]
    res = json.loads(ui_record_df.to_dict('records')[0]['page_configs'])

    return response_with(resp.SUCCESS_200, value={"data": res})


@ui_record_routes.route('/set_ui_record', methods=['POST'])
@jwt_required
def set_ui_record():
    try:
        user_id = get_jwt_identity()
        req_json = request.get_json()
        ui_configs = req_json['ui_configs']
        ui_record_query = db.session.query(Ui_record).filter(Ui_record.user_id == user_id)
        page_configs_str = json.dumps(ui_configs)
        if ui_record_query.count() <= 0:
            db.session.add(Ui_record(user_id=user_id, page_configs=page_configs_str))
        else:
            ui_record_query.update({'page_configs': page_configs_str})

        db.session.commit()
        return response_with(resp.SUCCESS_200)

    except Exception as e:
        db.session.rollback()
        return response_with(resp.MISSING_PARAMETERS_422)
