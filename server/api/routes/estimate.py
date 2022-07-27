from distutils.command.config import config
from flask import Blueprint
from flask import request
import pandas as pd

from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with
import math
estimate_routes = Blueprint("estimate_routes", __name__)

#小型車持有率
@estimate_routes.route('/owner_rate', methods=['POST'])
def owner_rate():

  infos_df = pd.read_sql(f"SELECT * FROM public.automobile_ownership;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )

#人口密度
@estimate_routes.route('/population_density', methods=['POST'])
def population_density():

  infos_df = pd.read_sql(f"SELECT * FROM public.population_density;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#戶籍人口數
@estimate_routes.route('/population', methods=['POST'])
def population():

  infos_df = pd.read_sql(f"SELECT count(*),geohash,point_s ,point_e ,point_w ,point_n  FROM public.population \
      where geohash <> 'w8h2n24' \
      group by geohash ,point_s ,point_e ,point_w ,point_n;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#停車場數
@estimate_routes.route('/parkingLot', methods=['POST'])
def parkingLot():

  infos_df = pd.read_sql(f"SELECT * FROM public.parkingLot ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#路邊停車格位數
@estimate_routes.route('/on_street', methods=['POST'])
def on_street():

  infos_df = pd.read_sql(f"select grid_id || '-' || 'on_street' as id,lat as latitude,lon as longitude FROM public.on_street_static ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#車站數
@estimate_routes.route('/station', methods=['POST'])
def station():

  infos_df = pd.read_sql(f"SELECT * FROM public.station ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#權利金估算
@estimate_routes.route('/estimate', methods=['POST'])
def estimate():
  X1=request.get_json()['X1']
  X2=request.get_json()['X2']
  X3=request.get_json()['X3']
  X4=request.get_json()['X4']
  X5=request.get_json()['X5']
  X6=request.get_json()['X6']
  X7=request.get_json()['X7']
  X8=request.get_json()['X8']
  X9=request.get_json()['X9']
  X10=request.get_json()['X10']
  X11=request.get_json()['X11']
  X12=request.get_json()['X12']
  X13=request.get_json()['X13']
  X14=request.get_json()['X14']
  X15=request.get_json()['X15']
  X16=request.get_json()['X16']
  X17=request.get_json()['X17']


  # infos_df = 875.195579+0.264*math.log(X1)-9.611*math.log(X2)-142.965*math.log(X3)+6.319*math.log(X4)-0.437*X5+5.038*math.log(X6)+12.2*X7-3.327*X8+7.575*X9+0.452*X10+1.206*X11-0.728*X12+7.665*X13-6.527*X14-3.728*X15-6.746*X16-16.567*X17-21.128*X18-22.824*X19
  infos_df=65.606+0.002*X1+0.0002714*X2+0.0002999*X3-2.658*X4+1.747*X5-0.016*X6+0.066*X7+3.586*X8+3.271*X9-0.398*X10-3.886*X11+8.181*X12+7.646*X13+9.544*X14-18.785*X15-20.527*X16-28.739*X17


  return response_with(resp.SUCCESS_200, value={"data": infos_df}, )

