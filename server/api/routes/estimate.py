from distutils.command.config import config
from flask import Blueprint
from flask import request
import pandas as pd
from api.utils.login_require import login_required
from api.utils import responses as resp
from api.utils.database import db
from api.utils.responses import response_with
import math
estimate_routes = Blueprint("estimate_routes", __name__)

#小型車持有率
@estimate_routes.route('/owner_rate', methods=['POST'])
@login_required
def owner_rate():

  infos_df = pd.read_sql(f"SELECT * FROM public.automobile_ownership;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )

#人口密度
@estimate_routes.route('/population_density', methods=['POST'])
@login_required
def population_density():

  infos_df = pd.read_sql(f"SELECT * FROM public.population_density;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#戶籍人口數
@estimate_routes.route('/population', methods=['POST'])
@login_required
def population():

  infos_df = pd.read_sql(f"SELECT * FROM public.population_result ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#停車場數
@estimate_routes.route('/parkingLot', methods=['POST'])
@login_required
def parkingLot():

  infos_df = pd.read_sql(f"SELECT * FROM public.parkingLot ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#路邊停車格位數
@estimate_routes.route('/on_street', methods=['POST'])
@login_required
def on_street():

  infos_df = pd.read_sql(f"select grid_id || '-' || 'on_street' as id,lat as latitude,lon as longitude FROM public.on_street_static ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#車站數
@estimate_routes.route('/station', methods=['POST'])
@login_required
def station():

  infos_df = pd.read_sql(f"SELECT * FROM public.station ;", con=db.engine)
  infos_dict = infos_df.to_dict('records')

  return response_with(resp.SUCCESS_200, value={"data": infos_dict}, )
#使用率估算
@estimate_routes.route('/estimate', methods=['POST'])
@login_required
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

#使用率估算(高)
@estimate_routes.route('/estimate_high', methods=['POST'])
@login_required
def estimate_high():
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

  infos_df=66.028+0.001*X2+0.0002*X3-1.048*X4-0.031*X6+6.518*X8+2.872*X9+4.479*X10-5.038*X11-0.492*X12-1.601*X13+12.975*X14-10.773*X15-8.219*X16-12.127*X17

  return response_with(resp.SUCCESS_200, value={"data": infos_df}, )
#使用率估算(中)
@estimate_routes.route('/estimate_mid', methods=['POST'])
@login_required
def estimate_mid():
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

  infos_df=55.210+0.001*X2-3.045*X4+4.316*X5-0.022*X6+17.808*X8+8.051*X10+7.532*X11+10.544*X13-25.450*X14-10.212*X16-25.452*X17
  return response_with(resp.SUCCESS_200, value={"data": infos_df}, )
#使用率估算(低)
@estimate_routes.route('/estimate_low', methods=['POST'])
@login_required
def estimate_low():
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

  infos_df=39.618+0.004*X1+0.0001*X2+0.0003*X3-2.880*X4-0.015*X6+0.539*X8+0.269*X9-3.893*X10-7.467*X11+17.444*X12+16.127*X13-1.723*X16-10.704*X17

  return response_with(resp.SUCCESS_200, value={"data": infos_df}, )
