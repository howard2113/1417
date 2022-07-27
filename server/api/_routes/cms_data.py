# -*- coding: utf-8 -*-
from flask import Blueprint
from flask import request
import pandas as pd
from api.models import cms_status
from api.models import cms_messages
from api.models import phrase
from api.models.cms_messages import CmsMessage, CmsMessageSchema
from api.models.phrase import Phrases, PhrasesSchema
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

cms_data_routes = Blueprint("cms_data_routes", __name__)

# 全部設備
@cms_data_routes.route('/infos', methods=['GET'])
def infos():  
  infos_df = pd.read_sql(f"SELECT * FROM cms_infos ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 設備狀態byid
@cms_data_routes.route('/device_status/<string:id>', methods=['GET'])
def device_status(id):  
  device_status_df = pd.read_sql(f"SELECT * FROM cms_status WHERE id='{id}';", con=db.engine)
  device_status_dict = device_status_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": device_status_dict}, )
# 讀取全部CMS訊息庫
@cms_data_routes.route('/device_messages', methods=['GET'])
def device_messages_GET():  
  device_messages_df = pd.read_sql(f"SELECT id, category, message, size, updatetime FROM cms_messages ;", con=db.engine)
  device_messages_dict = device_messages_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": device_messages_dict}, )

# 讀取CMS訊息庫 by id
@cms_data_routes.route('/device_messages/<string:id>', methods=['GET'])
def device_messages_GET_byid(id):  
  device_messages_df = pd.read_sql(f"SELECT * FROM cms_messages WHERE id={id} ;", con=db.engine)
  device_messages_dict = device_messages_df.to_dict('records')
  if len(device_messages_dict) != 0:
    # 把片語庫的對應片語找出來
    phrase_tuple = (device_messages_dict[0]['message_array'])
    result = Phrases.query.filter(Phrases.id.in_(phrase_tuple)).all()
    phrase_schema = PhrasesSchema(many=True)
    getData = phrase_schema.dump(result)
    device_messages_dict[0]['message_array'] = getData  

  return response_with(resp.SUCCESS_200, value={"data": device_messages_dict}, )

# 新增CMS訊息
@cms_data_routes.route('/device_messages', methods=['POST'])
def device_status_POST():  
  # 蒐集片語庫新id
  message_array = []
  # 片語insert
  for ph in request.json['data'][0]['message_array']:
    newPhrases = Phrases(
      ph['message'],
      ph['color'],
    )
    db.session.add(newPhrases)
    db.session.flush()
    message_array.append(newPhrases.id)
  # CMS訊息庫insert
  newDeviceMessage = CmsMessage(
    request.json['data'][0]['size'],
    request.json['data'][0]['category'],
    request.json['data'][0]['message'],
    request.json['data'][0]['color_array'],
    message_array,
    request.json['data'][0]['gearing'],
    request.json['data'][0]['updatetime'],
  )
  db.session.add(newDeviceMessage)
  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 修改CMS訊息
@cms_data_routes.route('/device_messages', methods=['PUT'])
def device_status_PUT(): 
  id = request.json['data'][0]['id']
  # 查詢舊CMS訊息的message_array
  device_messages_df = pd.read_sql(f"SELECT message_array FROM cms_messages WHERE id={id} ;", con=db.engine)
  device_messages_dict = device_messages_df.to_dict('records')
  # 刪除舊片語
  delete_phrases_tuple = (device_messages_dict[0]['message_array'])
  Phrases.query.filter(Phrases.id.in_(delete_phrases_tuple)).delete(synchronize_session='fetch')
  # 新增新片語
  message_array = []
  for ph in request.json['data'][0]['message_array']:
    newPhrases = Phrases(
      ph['message'],
      ph['color'],
    )
    db.session.add(newPhrases)
    db.session.flush()
    message_array.append(newPhrases.id)
  # 更新CMS訊息庫
  fetched = CmsMessage.query.filter(CmsMessage.id == request.json['data'][0]['id']).first()
  fetched.size = request.json['data'][0]['size']
  fetched.category =  request.json['data'][0]['category']
  fetched.message =  request.json['data'][0]['message']
  fetched.color_array =  request.json['data'][0]['color_array']
  fetched.message_array =  message_array
  fetched.gearing =  request.json['data'][0]['gearing']
  fetched.updatetime =  request.json['data'][0]['updatetime']
  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 刪除CMS訊息
@cms_data_routes.route('/device_messages/<string:id>', methods=['DELETE'])
def device_status_DELETE(id): 
  # 查詢舊CMS訊息的message_array
  device_messages_df = pd.read_sql(f"SELECT message_array FROM cms_messages WHERE id={id} ;", con=db.engine)
  device_messages_dict = device_messages_df.to_dict('records')
  # 如果沒有這個id
  if len(device_messages_dict) == 0:
    return response_with(resp.BAD_REQUEST_400, value={"data": "id error"}, )
  # 刪除舊片語
  delete_phrases_tuple = (device_messages_dict[0]['message_array'])
  Phrases.query.filter(Phrases.id.in_(delete_phrases_tuple)).delete(synchronize_session='fetch')  
  # 刪除CMS訊息庫
  CmsMessage.query.filter(CmsMessage.id == id).delete(synchronize_session='fetch')
  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )
