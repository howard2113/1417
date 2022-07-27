from flask import Blueprint
from flask import request
import pandas as pd
import uuid

from sqlalchemy.sql.elements import Null
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with

group_task_routes = Blueprint("group_task_routes", __name__)

# 全部群組
@group_task_routes.route('/grouplist', methods=['GET'])
def grouplist():  
  grouplist_df = pd.read_sql(f"SELECT DISTINCT ON (name) name, \
  prirorty, week_days, is_onece, start_date, start_time, \
  end_date, end_time, show_sec  FROM cms_task GROUP BY id, name;", con=db.engine)
  grouplist_dict = grouplist_df.to_dict('records')

  devicelist_df = pd.read_sql(f"SELECT cms_task.name, \
  cms_task.dev_id, cms_infos.location,  \
  cms_infos.size, cms_infos.lon, cms_infos.lat \
  FROM cms_task \
  LEFT JOIN cms_infos ON cms_task.dev_id = cms_infos.id WHERE cms_task.dev_id is not null ;", con=db.engine)
  devicelist_dict = devicelist_df.groupby('name').apply(lambda x: x.to_dict('records')).to_dict()
     
  for i in grouplist_dict:
    i['week_days'] = i['week_days'].split(',')
    if i['name'] in devicelist_dict:
      i['device'] = devicelist_dict[i['name']] # 合併設備基本資料

  return response_with(resp.SUCCESS_200, value={"data": grouplist_dict}, )

# 群組複製
@group_task_routes.route('/grouplist/copy', methods=['POST'])
def grouplist_copy_POST():
  name = request.json['name']
  new = str(request.json['new'])

  # 檢測是否重複
  if name == "":
    return response_with(resp.BAD_REQUEST_400, value={"data": "原始群組不存在"}, )
  
  cms_task_df = pd.read_sql(f"SELECT * FROM cms_task WHERE name='{name}';", con=db.engine)
  if cms_task_df.empty:
    return response_with(resp.BAD_REQUEST_400, value={"data": "原始群組不存在"}, )
  cms_task_df['name']=cms_task_df['name'].map({name:new})
  cms_task_df['id']=cms_task_df['id'].map(lambda x: uuid.uuid4())
  cms_task_df.set_index('id', inplace = True)
  cms_task_df.to_sql('cms_task', db.engine, if_exists='append')

  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 群組新增(空dev_id與空msg_id)
@group_task_routes.route('/grouplist', methods=['POST'])
def grouplist_POST():
  dict_group = {
    'id': uuid.uuid4(),
    'name': request.json['data'][0]['name'],
    'is_enable': True,
    'is_success': False,
    'prirorty': request.json['data'][0]['prirorty'],
    'week_days': ','.join(request.json['data'][0]['week_days']),
    'is_onece':  request.json['data'][0]['is_onece'],
    'start_date': request.json['data'][0]['start_date'],
    'start_time': request.json['data'][0]['start_time'],
    'end_date': request.json['data'][0]['end_date'],
    'end_time': request.json['data'][0]['end_time'],  
    'show_sec': request.json['data'][0]['show_sec'],  
  }

  dict_group_df = pd.DataFrame([dict_group])
  dict_group_df.set_index('id', inplace = True)
  dict_group_df.to_sql('cms_task', db.engine, if_exists='append')

  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 群組更新(包含基本資料與設備)
@group_task_routes.route('/grouplist', methods=['PUT'])
def grouplist_PUT():  
  name = request.json['data'][0]['name']
  groupinfo = request.json['data'][0]
  grouplist = []
  # 刪除name對應資料
  db.session.execute(f"DELETE FROM cms_task WHERE name = '{name}'")
  try: # 嘗試更新資料
    for device in groupinfo['dev_id']:
      grouplist.append({
        'id': uuid.uuid4(),
        'name': groupinfo['name'],
        'is_enable': True,
        'is_success': False,
        'prirorty': groupinfo['prirorty'],
        'week_days': ','.join(groupinfo['week_days']),
        'is_onece':  groupinfo['is_onece'],
        'start_date': groupinfo['start_date'],
        'start_time': groupinfo['start_time'],
        'end_date': groupinfo['end_date'],
        'end_time': groupinfo['end_time'],
        'dev_id': device
      })
    dict_group_df = pd.DataFrame(grouplist)
    dict_group_df.set_index('id', inplace = True)
    dict_group_df.to_sql('cms_task', db.engine, if_exists='append')

  except: # 更新失敗回滾並傳送
    db.session.rollback()
    return response_with(resp.BAD_REQUEST_400, value={"data": "更新失敗"}, )
  db.session.commit()
  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 群組刪除
@group_task_routes.route('/grouplist/<string:name>', methods=['DELETE'])
def grouplist_DELETE(name):
  # 刪除name對應資料
  db.session.execute(f"DELETE FROM cms_task WHERE name = '{name}'")
  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )

# 設備對應訊息取得
@group_task_routes.route('/devlist/<string:name>', methods=['GET'])
def devlist_GET(name):
  grouplist_df = pd.read_sql(f"SELECT cms_task.dev_id, \
  cms_task.msg_id  , cms_messages.message FROM cms_task \
  LEFT JOIN cms_messages ON cms_task.msg_id = cms_messages.id \
  WHERE cms_task.name='{name}' AND cms_task.msg_id is not null;", con=db.engine)
  grouplist_dict = grouplist_df.groupby('dev_id').apply(lambda x: x.to_dict('records')).to_dict()
  
  return response_with(resp.SUCCESS_200, value={"data": grouplist_dict}, )
  
# 設備變更
@group_task_routes.route('/devlist', methods=['PUT'])
def devlist_PUT():  
  name = request.json['data'][0]['name']
  devices = request.json['data'][0]['dev_id']
  # 取得群組基本資料
  grouplist_df = pd.read_sql(f"SELECT DISTINCT ON (name) name, \
  prirorty, week_days, is_onece, start_date, start_time, \
  end_date, end_time  FROM cms_task WHERE name='{name}' GROUP BY id, name ;", con=db.engine)
  grouplist_dict = grouplist_df.to_dict('records')
  
  deleteList = []
  cmstasklist = []
  for device in devices:
    deleteList.append("'" + device['dev_id'] + "'")
    if len(device['msg_id']) == 0:
      cmstasklist.append({
        'id': uuid.uuid4(),
        'name': grouplist_dict[0]['name'],
        'is_enable': True,
        'is_success': False,
        'prirorty': grouplist_dict[0]['prirorty'],
        'week_days': grouplist_dict[0]['week_days'],
        'is_onece':  grouplist_dict[0]['is_onece'],
        'start_date': grouplist_dict[0]['start_date'],
        'start_time': grouplist_dict[0]['start_time'],
        'end_date': grouplist_dict[0]['end_date'],
        'end_time': grouplist_dict[0]['end_time'],
        'dev_id': device['dev_id'],
        'msg_id': None
      })
    else:
      for msg in device['msg_id']:
        cmstasklist.append({
          'id': uuid.uuid4(),
          'name': grouplist_dict[0]['name'],
          'is_enable': True,
          'is_success': False,
          'prirorty': grouplist_dict[0]['prirorty'],
          'week_days': grouplist_dict[0]['week_days'],
          'is_onece':  grouplist_dict[0]['is_onece'],
          'start_date': grouplist_dict[0]['start_date'],
          'start_time': grouplist_dict[0]['start_time'],
          'end_date': grouplist_dict[0]['end_date'],
          'end_time': grouplist_dict[0]['end_time'],
          'dev_id': device['dev_id'],
          'msg_id': msg
        })

  # 刪除舊row
  deleteString = ','.join(deleteList)
  db.session.execute(f"DELETE FROM cms_task WHERE name = '{name}' AND \
    dev_id IN ({deleteString})")

  # 嘗試添加新row
  try: # 嘗試更新資料
    cmstask_df = pd.DataFrame(cmstasklist)
    cmstask_df.set_index('id', inplace = True)
    cmstask_df.to_sql('cms_task', db.engine, if_exists='append')

  except: # 更新失敗回滾並傳送
    db.session.rollback()
    return response_with(resp.BAD_REQUEST_400, value={"data": "更新失敗"}, )

  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )


# 設備刪除
@group_task_routes.route('/devlist/<string:name>/<string:dev_id>', methods=['DELETE'])
def devlist_DELETE(name, dev_id): 
  db.session.execute(f"DELETE FROM cms_task WHERE name = '{name}' AND \
    dev_id='{dev_id}'")
  db.session.commit() 
  return response_with(resp.SUCCESS_200, value={"data": ""}, )