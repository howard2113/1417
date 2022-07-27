# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request

from api.models.notify import NotifyHistory, NotifyHistorySchema
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

notify_routes = Blueprint("notify_routes", __name__)

@notify_routes.route('/getDate', methods=['GET','POST'])
def getDate():
    fetched = NotifyHistory.query.with_entities(NotifyHistory.update_time).distinct()
    NotifyHistory_schema = NotifyHistorySchema(many=True, only=['update_time'])
    NotifyHistorys = NotifyHistory_schema.dump(fetched)

    return response_with(resp.SUCCESS_200, value={"notify": NotifyHistorys},)

@notify_routes.route('/getData', methods=['GET','POST'])
def getData():
    getUpdateTime = request.args.get('update_time', None)
    fetched = NotifyHistory.query.filter_by(update_time=getUpdateTime)
    NotifyHistory_schema = NotifyHistorySchema(many=True, only=['device_id', 'type', 'first_error', 'address'])
    NotifyHistorys = NotifyHistory_schema.dump(fetched)

    total = []
    sql = "SELECT [type], COUNT(*) AS count FROM [thi_db].[dbo].[Notify] WHERE [address]!='' GROUP BY [type];"
    with db.engine.connect() as connection:
      CMSData = connection.execute(sql)
      for row in CMSData:
        total.append(dict(row))

    ans = {}
    sql = "SELECT [update_time], [etag1_now], [etag1_prev], [etag2_now], [etag2_prev], [etag3_now], [etag3_prev], [cms1_now], [cms1_prev], [tc1_now], [tc1_prev], [parking1_now], [parking2_prev], [parking2_now], [parking1_prev], [parking3_now], [parking3_prev] FROM [thi_db].[dbo].[NotifyMemory] WHERE [update_time] = '" + getUpdateTime + "';"
    with db.engine.connect() as connection:
      MemoryData = connection.execute(sql)
      if len(row) != 0:
        for row in MemoryData:
          ans = dict(row)

    return response_with(resp.SUCCESS_200, value={"notify": NotifyHistorys, "total": total, "memory": ans})

