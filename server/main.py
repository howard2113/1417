# -*- coding: utf-8 -*-
from flask import jsonify, send_from_directory
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
from flask_jwt_extended import (JWTManager, jwt_required)
from eventlet import wsgi
import eventlet
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from flask.json import JSONEncoder
from datetime import datetime
from api.routes.users import user_routes
# from api.routes.holidays import holiday_routes
# from api.routes.auth import auth_routes
# from api.routes.notify import notify_routes
# from api.routes.parking import parking_routes
# from api.routes.road import road_routes
# from api.routes.people import people_routes
# from api.routes.cctv import cctv_routes
# from api.routes.weather import weather_routes
# from api.routes.ui import ui_record_routes
# from api.routes.cms_data import cms_data_routes
# from api.routes.group import group_task_routes
from api.routes.parking import parking_routes
from api.routes.estimate import estimate_routes

from api.config.config import DevelopmentConfig, ProductionConfig, TestingConfig

import os, logging

from flask import Flask
from flask_compress import Compress
from flask import session


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.strftime('%Y/%m/%d %H:%M:%S')
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


SWAGGER_URL = '/api/docs'
app = Flask(__name__)
Compress(app)
CORS(app, supports_credentials=True)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)
app.config['JSON_AS_ASCII'] = False

db.init_app(app)
with app.app_context():
    db.create_all()
# app.register_blueprint(holiday_routes, url_prefix='/api/holiday')
app.register_blueprint(user_routes, url_prefix='/api/users')
# app.register_blueprint(auth_routes, url_prefix='/api/auth')
# app.register_blueprint(notify_routes, url_prefix='/api/notify')

# app.register_blueprint(parking_routes, url_prefix='/api/parking')
# app.register_blueprint(road_routes, url_prefix='/api/road')
# app.register_blueprint(people_routes, url_prefix='/api/people')
# app.register_blueprint(cctv_routes, url_prefix='/api/cctv')
# app.register_blueprint(weather_routes, url_prefix='/api/weather')
# app.register_blueprint(ui_record_routes, url_prefix='/api/ui')
# app.register_blueprint(cms_data_routes, url_prefix='/api/cms_data')
# app.register_blueprint(group_task_routes, url_prefix='/api/group_task')
app.register_blueprint(parking_routes, url_prefix='/api/parking')
app.register_blueprint(estimate_routes, url_prefix='/api/estimate')

app.json_encoder = CustomJSONEncoder
@app.route('/avatar/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


# # END GLOBAL HTTP CONFIGURATIONS

@app.route("/api/spec")
def spec():
    swag = swagger(app, prefix='/api')
    swag['info']['base'] = "http://localhost:5001"
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "Flask Author DB"
    return jsonify(swag)


swaggerui_blueprint = get_swaggerui_blueprint('/api/docs', '/api/spec', config={'app_name': "Flask Author DB"})
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
# 設定 JWT 密鑰
app.config['JWT_SECRET_KEY'] = 'COA_y4e3xzVd59yr68ePvQwVDEWPl34cczGDdwfeWtNJYjoF2r1rnYp6abFK_Vtzl3i_LrtqfuDV9tTtDUOuBQ'
app.config['JWT_ALGORITHM'] = 'HS256'
# app.config['JWT_IDENTITY_CLAIM'] = 'exp'
jwt = JWTManager(app)
jwt.init_app(app)

db.init_app(app)
# # mail.init_app(app)
with app.app_context():
    #     # from api.models import *
    db.create_all()

if __name__ == "__main__":
    # app.run(port=5000, host="0.0.0.0", use_reloader=False)
    wsgi.server(eventlet.listen(('0.0.0.0', 5002)), app)
