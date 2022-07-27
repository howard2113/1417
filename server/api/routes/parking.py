# -avg(usage)as usage,avg(space)as space,avg(supply)as supply- coding: utf-8 -avg(usage)as usage,avg(space)as space,avg(supply)as supply-
from distutils.command.config import config
from flask import Blueprint
from flask import request
import pandas as pd

from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with
import math
parking_routes = Blueprint("parking_routes", __name__)

# 供需usage(id)
@parking_routes.route('/sd_usage', methods=['POST'])
def sd_usage():

  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  holiday= ','.join(request.get_json()['holidays'])
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  type= ','.join(request.get_json()['type'])
  infos_df = pd.read_sql(f"select avg({hour})/{len(request.get_json()['hour'])} as usage,car_type,count(distinct area) as count_id \
    from sd_usage \
    where area in {id} and is_workday in ({holiday}) and car_type in ({type}) group by car_type;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 供需usage(district)
@parking_routes.route('/sd_usage_district', methods=['POST'])
def sd_usage_district():

  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  holiday= ','.join(request.get_json()['holidays'])
  type= ','.join(request.get_json()['type'])
  infos_df = pd.read_sql(f"select avg({hour})/{len(request.get_json()['hour'])} as usage,car_type,count(distinct area) as count_id \
    from sd_usage \
    where district in {district} and is_workday in ({holiday}) and car_type in ({type}) group by car_type;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 供需supply(id)
@parking_routes.route('/sd_supply', methods=['POST'])
def sd_supply():

  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  holiday= ','.join(request.get_json()['holidays'])
  type= ','.join(request.get_json()['type'])
  infos_df = pd.read_sql(f"select avg({hour})/{len(request.get_json()['hour'])} as supply,car_type,count(distinct area) as count_id \
    from sd_supply \
    where area in {id} and is_workday in ({holiday}) and car_type in ({type}) group by car_type;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 供需supply(district)
@parking_routes.route('/sd_supply_district', methods=['POST'])
def sd_supply_district():

  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  holiday= ','.join(request.get_json()['holidays'])
  type= ','.join(request.get_json()['type'])
  infos_df = pd.read_sql(f"select avg({hour})/{len(request.get_json()['hour'])} as supply,car_type,count(distinct area) as count_id \
    from sd_supply \
    where district in {district} and is_workday in ({holiday}) and car_type in ({type}) group by car_type;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 供需totalcar
@parking_routes.route('/sd_totalcar', methods=['POST'])
def sd_totalcar():

  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  holiday= ','.join(request.get_json()['holidays'])
  type= ','.join(request.get_json()['type'])
  infos_df=pd.read_sql(f"select sum(totalcar)as totalcar,car_type,count(distinct area) as count_id from (\
select area,sum({hour})/{len(request.get_json()['hour'])} as totalcar,car_type     \
from sd_totalcar \
where area in {id} and is_workday in ({holiday}) and car_type in ({type}) group by car_type,area \
)as a \
group by car_type;", con=db.engine)
  print(infos_df)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 供需totalcar(district)
@parking_routes.route('/sd_totalcar_district', methods=['POST'])
def sd_totalcar_district():

  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  holiday= ','.join(request.get_json()['holidays'])
  type= ','.join(request.get_json()['type'])
  infos_df=pd.read_sql(f"select sum(totalcar)as totalcar,car_type,count(distinct area) as count_id from (\
select area,sum({hour})/{len(request.get_json()['hour'])} as totalcar,car_type     \
from sd_totalcar \
where district in {district} and is_workday in ({holiday}) and car_type in ({type}) group by car_type,area \
)as a \
group by car_type;", con=db.engine)
  print(infos_df)
  infos_dict = infos_df.to_dict('records')
  print(infos_dict)

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#供需id
@parking_routes.route('/sd_id', methods=['POST'])
def sd_id():
  infos_df = pd.read_sql(f"select distinct area as id,district from sd_usage ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#供需經緯
@parking_routes.route('/sd_xy', methods=['POST'])
def sd_xy():
  infos_df = pd.read_sql(f"select area as id,district,type,x as longitude,y as latitude from area_coordinate where type=0;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊id
@parking_routes.route('/on_street_id', methods=['POST'])
def on_street_id():
  config={'板橋區':1,"中和區":2,"新莊區":3,"三重區":4,"新店區":5,"土城區":6,"永和區":7,"蘆洲區":8,"汐止區":9,"樹林區":10,
  "淡水區":11,"三峽區":12,"鶯歌區":13,"林口區":14,"五股區":15,"泰山區":16,"瑞芳區":17,"八里區":18,"深坑區":19,"三芝區":20
  ,"金山區":21,"萬里區":22,"貢寮區":23,"石門區":24,"雙溪區":25,"石碇區":26,"坪林區":27,"烏來區":28,"平溪區":29}
  infos_df = pd.read_sql(f"select distinct road_id as id,district,road_name as name from on_street_static;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in range (len(infos_dict)):
    infos_dict[i]['district']=config[infos_dict[i]['district']]
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊經緯
@parking_routes.route('/on_street_xy', methods=['POST'])
def on_street_xy():
  # latitude: 25.075495, longitude: 121.36758
  config={'板橋區':1,"中和區":2,"新莊區":3,"三重區":4,"新店區":5,"土城區":6,"永和區":7,"蘆洲區":8,"汐止區":9,"樹林區":10,
  "淡水區":11,"三峽區":12,"鶯歌區":13,"林口區":14,"五股區":15,"泰山區":16,"瑞芳區":17,"八里區":18,"深坑區":19,"三芝區":20
  ,"金山區":21,"萬里區":22,"貢寮區":23,"石門區":24,"雙溪區":25,"石碇區":26,"坪林區":27,"烏來區":28,"平溪區":29}
  infos_df = pd.read_sql(f"select road_id as id,district,road_name,lat as latitude,lon as longitude from on_street_static;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in range (len(infos_dict)):
    infos_dict[i]['district']=config[infos_dict[i]['district']]
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊usage
@parking_routes.route('/on_street_usage', methods=['POST'])
def on_street_usage():
  start=request.get_json()['start']
  end=request.get_json()['end']
  holidays=','.join(request.get_json()['holidays'])
  hour=','.join(request.get_json()['hour'])
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"(select '0'as car_type,(sum(totalstay)/sum(cnt*60))*100 as usage, count(distinct officialid)as count_id \
    from on_street_dynamic_hour_vehicle \
    left join holidays h on date(date_col) = date(infotime) \
    where infotime::date between '{start}' and '{end}' and officialid  in {id} \
    and h.is_workday in ({holidays}) and extract(hour from  infotime) in ({hour})) \
    union ALL \
    (select '1'as car_type,(sum(totalstay)/sum(cnt*60))*100 as usage , count(distinct officialid)as count_id \
    from on_street_dynamic_hour_special_vehicle \
    left join holidays h on date(date_col) = date(infotime) \
    where infotime::date between '{start}' and '{end}' and officialid  in {id} \
    and h.is_workday in ({holidays}) and extract(hour from  infotime) in ({hour}))  ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  print(infos_dict)
  for i in infos_dict:
    if(pd.isna(i['usage'])):
      i['usage']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊usage(days)
@parking_routes.route('/on_street_usage_days', methods=['POST'])
def on_street_usage_days():
  start=request.get_json()['start']
  end=request.get_json()['end']
  holidays=','.join(request.get_json()['holidays'])
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"(select '0'as car_type,(sum(park_times)/sum(charging_hrs))*100 as usage, count(distinct officialid)as count_id \
    from on_street_dynamic_days \
    left join holidays h on date(date_col) = date(infodate) \
    where infodate::date between '{start}' and '{end}' and officialid  in {id} and name_type in(3,4,5) \
    and h.is_workday in ({holidays}) ) \
    union ALL \
    (select '1'as car_type,(sum(park_times)/sum(charging_hrs))*100 as usage , count(distinct officialid)as count_id \
    from on_street_dynamic_days \
    left join holidays h on date(date_col) = date(infodate) \
    where infodate::date between '{start}' and '{end}' and officialid  in {id} and name_type in(1) \
    and h.is_workday in ({holidays}) )  ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  print(infos_dict)
  for i in infos_dict:
    if(pd.isna(i['usage'])):
      i['usage']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊supply
@parking_routes.route('/on_street_supply', methods=['POST'])
def on_street_supply():
  start=request.get_json()['start']
  end=request.get_json()['end']
  holidays=','.join(request.get_json()['holidays'])
  hour=','.join(request.get_json()['hour'])
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select  '0' as car_type,(sum(totalcar))::float8 /sum(cnt)::float8 as supply, count(distinct officialid)as count_id \
    from on_street_dynamic_hour_vehicle \
    left join holidays h on date(date_col) = date(infotime) \
    where infotime::date between '{start}' and '{end}' and officialid  in {id} \
    and h.is_workday in ({holidays}) and extract(hour from  infotime) in ({hour}) \
    union ALL \
    select '1' as car_type,(sum(totalcar))::float8 /sum(cnt)::float8 as supply, count(distinct officialid)as count_id \
    from on_street_dynamic_hour_special_vehicle \
    left join holidays h on date(date_col) = date(infotime) \
    where infotime::date between '{start}' and '{end}' and officialid  in {id}\
    and h.is_workday in ({holidays}) and extract(hour from  infotime) in ({hour})  ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(pd.isna(i['supply'])):
      i['supply']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊totalcar
@parking_routes.route('/on_street_totalcar', methods=['POST'])
def on_street_totalcar():
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select '0' as car_type,sum(count) as totalcar,count(distinct road_id)as count_id from( \
    select road_id,count(name_cnt)  from grid_charge_type_statics \
    where road_id in {id} and name_type in ('汽車停車位','家長接送區','時段性禁停停車位') \
    group by name_type ,road_id \
    )as a \
    union All \
    select '1' as car_type,sum(count) as totalcar,count(distinct road_id)as count_id from(  \
    select road_id,count(name_cnt)  from grid_charge_type_statics  \
    where road_id in {id} and name_type in ('汽車身心障礙專用') \
    group by name_type ,road_id \
    )as b ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(math.isnan(i['totalcar'])):
      i['totalcar']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路邊revenue
@parking_routes.route('/on_street_revenue', methods=['POST'])
def on_street_revenue():
  holidays=','.join(request.get_json()['holidays'])
  start=request.get_json()['start']
  end=request.get_json()['end']
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select '0' as car_type, sum(amount)as revenue,count(distinct officialid)as count_id from on_street_dynamic_days \
    left join holidays h on date(date_col) = date(infodate) \
    where officialid in {id} and name_type in (3,4,5) and infodate between '{start}' and '{end}' \
    and h.is_workday in ({holidays})  \
    union All \
    select '1' as car_type, sum(amount)as revenue,count(distinct officialid)as count_id from on_street_dynamic_days \
    left join holidays h on date(date_col) = date(infodate) \
    where officialid in {id} and name_type in (1) and infodate between '{start}' and '{end}' \
    and h.is_workday in ({holidays})  \
;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(i['revenue']is None or math.isnan(i['revenue'])):
      i['revenue']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合usage
@parking_routes.route('/multi_usage', methods=['POST'])
def multi_usage():
  holidays=','.join(request.get_json()['holidays'])
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  start=request.get_json()['start']
  end=request.get_json()['end']
  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")

  infos_df=pd.read_sql(f"select car_type, avg({hour})/{len(request.get_json()['hour'])} as usage from multi_total_usage \
    left join holidays h on date(date_col) = date(infotime) \
    where  district in {district}  and infotime between '{start}' and '{end}' and car_type in (2,3) \
    and h.is_workday in ({holidays})   group by car_type \
    union all \
    select car_type, avg({hour})/{len(request.get_json()['hour'])} as usage from sd_usage \
    where  district in  {district}  and  car_type=5  group by car_type", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(i['usage']is None or math.isnan(i['usage'])):
      i['usage']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合supply
@parking_routes.route('/multi_supply', methods=['POST'])
def multi_supply():
  holidays=','.join(request.get_json()['holidays'])
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  start=request.get_json()['start']
  end=request.get_json()['end']
  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")

  infos_df=pd.read_sql(f"select car_type, avg({hour})/{len(request.get_json()['hour'])} as supply from multi_total_supply \
    left join holidays h on date(date_col) = date(infotime) \
    where  district in {district}  and infotime between '{start}' and '{end}' and car_type in (2,3) \
    and h.is_workday in ({holidays})   group by car_type \
    union all \
    select car_type, avg({hour})/{len(request.get_json()['hour'])} as supply from sd_supply \
    where  district in  {district}  and  car_type=5  group by car_type", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(i['supply']is None or math.isnan(i['supply'])):
      i['supply']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合totalcar
@parking_routes.route('/multi_totalcar', methods=['POST'])
def multi_totalcar():
  holidays=','.join(request.get_json()['holidays'])
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour='+'.join(hour)
  start=request.get_json()['start']
  end=request.get_json()['end']
  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")

  infos_df=pd.read_sql(f"select car_type, sum({hour})/{len(request.get_json()['hour'])} as totalcar from multi_total_totalcar \
    left join holidays h on date(date_col) = date(infotime) \
    where  district in {district}  and infotime between '{start}' and '{end}' and car_type in (2,3) \
    and h.is_workday in ({holidays})   group by car_type \
    union all \
    select car_type, sum({hour})/{len(request.get_json()['hour'])} as totalcar from sd_totalcar \
    where  district in  {district}  and  car_type=5  group by car_type", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(i['totalcar']is None or math.isnan(i['totalcar'])):
      i['totalcar']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合totalcar(地圖框選)
@parking_routes.route('/multi_totalcar_map', methods=['POST'])
def multi_totalcar_map():
  ids = list(set(request.get_json()['id']))
  hour_arr=request.get_json()['hour']
  hour=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour.append(h)
  hour_str='+'.join(hour)
  holiday= request.get_json()['holidays']
  area_ids = []
  off_ids = []
  on_ids = []
  for i in ids:
      if len(i) == 8:
          area_ids.append(i)
      elif len(i) == 6:
          off_ids.append(i)
      else:
          on_ids.append(i)
  params ={}
  params['area_ids'] = tuple(area_ids) if len(area_ids) > 0 else ('',)
  params['off_ids'] = tuple(off_ids) if len(off_ids) > 0 else ('',)
  params['on_ids'] = tuple(on_ids) if len(on_ids) > 0 else ('',)
  params['holiday'] = tuple(holiday)
  sql = f"""with
        -- 抓取表multi_sd_supply,計算時間區段內平均停車格數(0 :大型車, 1 :自行車, 2 :汽車, 3 :特殊汽車, 4 :特殊機車, 5 :機車)
        step1_1 as (select sum({hour_str})/{len(hour)} as totalcar,car_type,count(distinct area) as count_id
                from multi_sd_supply
                where area in %(area_ids)s and is_workday in %(holiday)s
                group by car_type),
        step1_2 as (select a.car_type, step1_1.totalcar, step1_1.count_id
                    from (select distinct car_type from multi_sd_supply) as a
                    left join step1_1 on step1_1.car_type = a.car_type),
        -- 抓取路邊停車格(小客車)
        step2_1 as (select road_id,count(grid_id) as c
                  from on_street_static
                  where road_id in %(on_ids)s and name in ('汽車停車位','家長接送區','時段性禁停停車位')
                  group by road_id),
        -- 抓取路邊停車格(特殊車)
        step2_2 as (select road_id,count(grid_id) as c
                  from on_street_static
                  where road_id in %(on_ids)s and name in ('汽車身心障礙專用')
                  group by road_id),
        -- 合併路邊停車格數量
        step2_3 as (select 2 as car_type, sum(c) as totalcar, count(distinct road_id) as count_id
                    from step2_1
                    union All
                    select 3 as car_type, sum(c) as totalcar, count(distinct road_id) as count_id
                    from step2_2),
        -- 抓取路外停車格(小客車及機車)
        step3_1 as (select sum(totalcar) as totalcar, sum(totalmotor) as totalmotor, count(distinct id) as count_id
                  from off_street_static
                  where id in %(off_ids)s),
        -- 轉置路外停車格資料,加上car_type
        step3_2 as (select step3_1.count_id, t.*
                    from step3_1
                    cross join lateral (
                      values
                        (step3_1.totalcar, 2),
                        (step3_1.totalmotor, 5)
                    ) as t(totalcar, car_type)),
        -- 抓取路外停車格(特殊車-身障))
        step4 as (select 3 as car_type, sum(disability_car) as totalcar, count(distinct parking_id)as count_id
                  from off_street_parkings
                  where parking_id in %(off_ids)s)
        -- 合併所有資料表
        select step1_2.car_type, coalesce(step1_2.count_id,0)+coalesce(step2_3.count_id,0)+coalesce(step3_2.count_id,0)+coalesce(step4.count_id,0) as count_id,
               coalesce(step1_2.totalcar,0)+coalesce(step2_3.totalcar,0)+coalesce(step3_2.totalcar,0)+coalesce(step4.totalcar,0) as totalcar
        from step1_2
        LEFT JOIN step2_3 ON step1_2.car_type = step2_3.car_type
        LEFT JOIN step3_2 ON step1_2.car_type = step3_2.car_type
        LEFT JOIN step4 ON step1_2.car_type = step4.car_type;
  """
  infos_df=pd.read_sql(sql, con=db.engine, params=params)
  blank_df = pd.DataFrame([{'car_type': 2}, {'car_type': 3}, {'car_type': 5}])
  infos_df = pd.merge(blank_df, infos_df, how='left', on='car_type')
  infos_df.fillna('nan', inplace=True)
  infos_dict = infos_df.to_dict('records')
  return response_with(resp.SUCCESS_200, value={'data':infos_dict})
# 綜合revenue
@parking_routes.route('/multi_revenue', methods=['POST'])
def multi_revenue():
  holidays=','.join(request.get_json()['holidays'])
  config={'板橋區':1,"中和區":2,"新莊區":3,"三重區":4,"新店區":5,"土城區":6,"永和區":7,"蘆洲區":8,"汐止區":9,"樹林區":10,
  "淡水區":11,"三峽區":12,"鶯歌區":13,"林口區":14,"五股區":15,"泰山區":16,"瑞芳區":17,"八里區":18,"深坑區":19,"三芝區":20
  ,"金山區":21,"萬里區":22,"貢寮區":23,"石門區":24,"雙溪區":25,"石碇區":26,"坪林區":27,"烏來區":28,"平溪區":29}
  if(len(request.get_json()['district'])>1):
    district= tuple(request.get_json()['district'])
  else:
    district=str(tuple(request.get_json()['district']))
    district=district.replace(",", "")
  start=request.get_json()['start']
  end=request.get_json()['end']
  is_day=request.get_json()['is_day']
  district_array=[]
  inv_dict = {value:key for key, value in config.items()}
  print(inv_dict[5])
  for i in request.get_json()['district']:
    district_array.append(inv_dict[int(i)])
  if(len(district_array)>1):
    district= tuple(district_array)
  else:
    district=str(tuple(district_array))
    district=district.replace(",", "")
  #汽車部分 日:路邊 月或年:路邊+路外
  if(is_day=="true"):
    infos_df=pd.read_sql(f"select '0' as car_type, sum(amount)as revenue \
from( \
    select distinct(a.officialid),a.infodate ,a.name_type,a.bill_number,a.park_times,a.amount,a.charging_hrs ,a.cnt,b.district \
    from on_street_dynamic_days  as a \
    inner join on_street_static as b on a.officialid  = b.road_id \
    )as c \
    left join holidays h on date(date_col) = date(c.infodate)  \
where  district  in {district} and  name_type in (3,4,5) and c.infodate between '{start}' and '{end}' \
and h.is_workday in ({holidays})   \
union All \
select '1' as car_type, sum(amount)as revenue from on_street_dynamic_days as a \
left join holidays h on date(date_col) = date(infodate)  left join on_street_static oss on officialid  = road_id \
where  district  in {district} and  name_type in (1) and a.infodate between '{start}' and '{end}' \
and h.is_workday in ({holidays})", con=db.engine)
  else:
    infos_df=pd.read_sql(f"select '0'as car_type, sum(revenue)as revenue from( \
select '0' as car_type,sum(total_revenue)as revenue \
from( \
select distinct  parking_id,parking_register,total_revenue, TO_TIMESTAMP(year+1911||'-'||month,'YYYY-MM') AS dateCol ,oss.area \
from off_street_register_to_id osrti left join off_street_static oss on parking_id =id \
where area in{district} \
)as a  \
where a.dateCol between '{start}' and '{end}' \
union all \
select '0' as car_type, sum(amount)as revenue \
from( \
    select distinct(a.officialid),a.infodate ,a.name_type,a.bill_number,a.park_times,a.amount,a.charging_hrs ,a.cnt,b.district \
    from on_street_dynamic_days  as a \
    inner join on_street_static as b on a.officialid  = b.road_id \
    )as c \
    left join holidays h on date(date_col) = date(c.infodate)  \
where  district  in {district} and  name_type in (3,4,5) and c.infodate between '{start}' and '{end}' \
and h.is_workday in ({holidays})  ) as x \
union All \
select '1' as car_type, sum(amount)as revenue from on_street_dynamic_days as a \
left join holidays h on date(date_col) = date(infodate)  left join on_street_static oss on officialid  = road_id \
where  district  in {district} and  name_type in (1) and a.infodate between '{start}' and '{end}' \
and h.is_workday in ({holidays})", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in infos_dict:
    if(i['revenue']is None or math.isnan(i['revenue'])):
      i['revenue']='nan'
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合使用率需供率(地圖框選)
@parking_routes.route('/multi_usage_supply_map', methods=['POST'])
def multi_usage_supply_map():
  start=request.get_json()['start']
  end=request.get_json()['end']
  holidays=','.join(request.get_json()['holidays'])
  #一般小時
  hour=','.join(request.get_json()['hour'])
  ids = list(set(request.get_json()['id']))
  area_ids = []
  off_ids = []
  on_ids = []
  for i in ids:
      if len(i) == 8:
          area_ids.append(i)
      elif len(i) == 6:
          off_ids.append(i)
      else:
          on_ids.append(i)
  params ={}
  params['area_ids'] = tuple(area_ids) if len(area_ids) > 0 else ("('')")
  params['off_ids'] = tuple(off_ids) if len(off_ids) > 0 else ("('')")
  params['on_ids'] = tuple(on_ids) if len(on_ids) > 0 else ("('')")
  # 供需用小時(hr_8...)
  hour_arr=request.get_json()['hour']
  hour_hr=[]
  for h in hour_arr:
    h='hr_'+str(h)
    hour_hr.append(h)
  hour_hr='+'.join(hour_hr)
  print(hour_hr)
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"with \
supply_table as( \
select sum(supply)as total_supply ,car_type from ( \
select sum({hour_hr})as supply ,car_type from multi_sd_supply \
where area in {params['area_ids']} and car_type in(2,3,5) group by car_type \
union all  \
select sum(cnt)as supply,'2' as car_type  from on_street_dynamic_hour_vehicle osdhv  \
left join holidays h on date(date_col) = date(infotime)   \
where officialid in {params['on_ids']} and infotime between '{start}' and '{end}'  and h.is_workday in ({holidays}) \
and extract(hour from  infotime) in ({hour}) \
union all  \
select sum(cnt)as supply,'3' as car_type  from on_street_dynamic_hour_special_vehicle osdhsv  \
left join holidays h on date(date_col) = date(infotime)   \
where officialid in {params['on_ids']} and infotime between '{start}' and '{end}'  and h.is_workday in ({holidays}) \
and extract(hour from  infotime) in ({hour}) \
union all  \
select sum(totalcar)* {len(request.get_json()['hour'])} as supply,'2' as car_type from Off_street_static  \
where id in {params['off_ids']}  \
)as a group by a.car_type \
), \
demand_table as( \
select sum(demand)as total_demand ,car_type from ( \
select sum({hour_hr})as demand ,car_type from multi_sd_demand msd  \
where area in ('02012001') and car_type in(2,3,5) group by car_type \
union all  \
select sum(totalcar)as demand,'2' as car_type  from on_street_dynamic_hour_vehicle osdhv  \
left join holidays h on date(date_col) = date(infotime)   \
where officialid in {params['on_ids']} and infotime between '{start}' and '{end}'  and h.is_workday in ({holidays}) \
and extract(hour from  infotime) in ({hour}) \
union all  \
select sum(totalcar)as demand,'3' as car_type  from on_street_dynamic_hour_special_vehicle osdhsv  \
left join holidays h on date(date_col) = date(infotime)   \
where officialid in {params['on_ids']} and infotime between '{start}' and '{end}'  and h.is_workday in ({holidays}) \
and extract(hour from  infotime) in ({hour}) \
union all  \
select sum(totalcar)as demand,'2' as car_type from off_street_dynamic_hours osdh  \
left join holidays h on date(date_col) = date(infotime)   \
where id in {params['off_ids']} and infotime between '{start}' and '{end}'  and h.is_workday in ({holidays}) \
and extract(hour from  infotime) in ({hour}) \
)as a group by a.car_type \
) \
select total_supply, total_demand, supply_table.car_type  \
from supply_table LEFT join demand_table on supply_table.car_type = demand_table.car_type ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 綜合revenue(地圖框選)
@parking_routes.route('/multi_revenue_map', methods=['POST'])
def multi_revenue_map():
  ids = list(set(request.get_json()['id']))
  start=request.get_json()['start']
  end=request.get_json()['end']
  is_day=request.get_json()['is_day']
  holiday= request.get_json()['holidays']
  params ={}
  off_ids = []
  on_ids = []
  for i in ids:
      if len(i) == 6:
          off_ids.append(i)
      elif len(i)<6:
          on_ids.append(i)
  params['off_ids'] = tuple(off_ids) if len(off_ids) > 0 else ('',)
  params['on_ids'] = tuple(on_ids) if len(on_ids) > 0 else ('',)
  params['holiday'] = tuple(holiday)
  params['start'] = start
  params['end'] = end
  sql = f"""with
      -- 抓取路邊所選區間內的amount資料, 依照name_type分成小客車(0)及特殊車-身障(1)
      step1_1 as (select officialid, infodate , amount,
                        CASE
                        WHEN name_type in (3,4,5) THEN '0'
                        WHEN name_type in (1) THEN '1'
                        ELSE '2'
                        END AS car_type
                from on_street_dynamic_days as a
                left join holidays on date(holidays.date_col) = date(a.infodate)
                where a.officialid in %(on_ids)s and a.infodate between %(start)s and %(end)s and holidays.is_workday in %(holiday)s),
      -- 加總amount
      step1_2 as (select car_type,sum(amount) as revenue from step1_1
                where car_type in ('0','1')
                group by car_type)
  """
  if is_day == "true":
      sql = sql+"select * from step1_2;"
  else:
    sql = sql+f"""
        -- 抓取路外月資料(若同id,year,month有不同total_revenue,取最大的)
        ,step2_1 as (select parking_id, max(total_revenue) as total_revenue, year, month
                    from off_street_register_to_id
                    where parking_id in %(off_ids)s
                    group by parking_id, year, month),
        -- 加總revenue, 給定car_type=0
        step2_2 as (select '0' as car_type, sum(total_revenue) as revenue from step2_1
                    where CAST(year+1911||'-'||month||'-1' AS DATE) between %(start)s and %(end)s )
        -- 合併路邊及路外資料
        select data.car_type, sum(data.revenue) as revenue
        from (select * from step1_2 union all select * from step2_2) as data
        group by data.car_type;
    """
  infos_df=pd.read_sql(sql, con=db.engine, params=params)
  blank_df = pd.DataFrame([{'car_type': '0'}, {'car_type': '1'}])
  infos_df = pd.merge(blank_df, infos_df, how='left', on='car_type')
  infos_df.fillna(0, inplace=True)
  infos_dict = infos_df.to_dict('records')
  return response_with(resp.SUCCESS_200, value={'data':infos_dict})
# 路外
@parking_routes.route('/off_street', methods=['POST'])
def off_street():
  start=request.get_json()['start']
  end=request.get_json()['end']
  holidays=','.join(request.get_json()['holidays'])
  hour=','.join(request.get_json()['hour'])
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select avg(usage)*100 as usage,avg(supply)as supply,count(distinct a.id)as count_id \
from off_street_dynamic_hours as a \
left join off_street_static as b on a.id=b.id \
left join holidays h on date(date_col) = date(infotime) \
where infotime between '{start}' and '{end}' and a.id in {id}  and a.type=2 \
and h.is_workday in ({holidays}) and extract(hour from  infotime) in ({hour})  ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路外合法停車格位數(席)
@parking_routes.route('/off_street_totalcar', methods=['POST'])
def off_street_totalcar():
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select sum(totalcar),count(distinct id)as count_id \
  from off_street_static \
  where id in {id};", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路外經緯
@parking_routes.route('/off_street_xy', methods=['POST'])
def off_street_xy():

  config={'板橋區':1,"中和區":2,"新莊區":3,"三重區":4,"新店區":5,"土城區":6,"永和區":7,"蘆洲區":8,"汐止區":9,"樹林區":10,
  "淡水區":11,"三峽區":12,"鶯歌區":13,"林口區":14,"五股區":15,"泰山區":16,"瑞芳區":17,"八里區":18,"深坑區":19,"三芝區":20
  ,"金山區":21,"萬里區":22,"貢寮區":23,"石門區":24,"雙溪區":25,"石碇區":26,"坪林區":27,"烏來區":28,"平溪區":29}
  infos_df = pd.read_sql(f"select id,area as district,longitude,latitude from off_street_static;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  for i in range (len(infos_dict)):
    infos_dict[i]['district']=config[infos_dict[i]['district']]
  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路外 收費金額估算
@parking_routes.route('/off_street_revenue', methods=['POST'])
def off_street_revenue():
  start=request.get_json()['start']
  end=request.get_json()['end']
  if(len(request.get_json()['id'])>1):
    id= tuple(request.get_json()['id'])
  else:
    id=str(tuple(request.get_json()['id']))
    id=id.replace(",", "")

  infos_df = pd.read_sql(f"select sum(total_revenue)as revenue,count(distinct parking_id)as count_id \
from(select distinct  parking_id,parking_register,total_revenue, TO_TIMESTAMP(year+1911||'-'||month,'YYYY-MM') AS dateCol \
from off_street_register_to_id osrti \
)as a \
where a.dateCol between '{start}'and'{end}' and parking_id in  {id};", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
# 路外ID
@parking_routes.route('/off_street_id', methods=['POST'])
def off_street_id():

  infos_df = pd.read_sql(f"select id,area as district,name from off_street_static ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')
  config={'板橋區':1,"中和區":2,"新莊區":3,"三重區":4,"新店區":5,"土城區":6,"永和區":7,"蘆洲區":8,"汐止區":9,"樹林區":10,
  "淡水區":11,"三峽區":12,"鶯歌區":13,"林口區":14,"五股區":15,"泰山區":16,"瑞芳區":17,"八里區":18,"深坑區":19,"三芝區":20
  ,"金山區":21,"萬里區":22,"貢寮區":23,"石門區":24,"雙溪區":25,"石碇區":26,"坪林區":27,"烏來區":28,"平溪區":29}
  for i in range (len(infos_dict)):
    infos_dict[i]['district']=config[infos_dict[i]['district']]



  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
