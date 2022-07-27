import os.path
import numpy as np
import time
import requests
import json
import random
from datetime import datetime, timedelta
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text, DateTime, Float, BigInteger, REAL
from util.database import mysql2csv

Base = declarative_base()
engine = create_engine(f"mysql+pymysql://thia01:thiits@localhost:3306/imageprocess", echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)



# header = ['DeviceID', 'DeliverTime', 'DetectID', 'CarID', 'CarType', 'InTime', 'OutTime', 'CType']
# sub_grid_area = pd.read_csv(r"CDRawdata.csv", header=None, names=header)
# sub_grid_area.to_sql('CDRawdata', engine, if_exists='append', index=False, chunksize=500)

header = ['UniId', 'CarType']
sub_grid_area = pd.read_csv(r"CarTypeInfo.csv", header=None, names=header)
sub_grid_area.replace(r'\\N', np.nan, regex=True, inplace=True)
sub_grid_area.to_sql('CarTypeInfo', engine, if_exists='append', index=False, chunksize=500)

# header = ['timestamp', 'id', 'obuid', 'speed', 'heading', 'lon', 'lat', 'obu_lon', 'obu_lat']
# sub_grid_area = pd.read_csv(r"ITRIbsm.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIbsm', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'cms_id', 'status', 'total']
# sub_grid_area = pd.read_csv(r"ITRIcms_log.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIcms_log', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'cms_id', 'status', 'total']
# sub_grid_area = pd.read_csv(r"ITRIcms_log05.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIcms_log05', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'cms_id', 'status', 'total']
# sub_grid_area = pd.read_csv(r"ITRIcms_log15.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIcms_log15', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'cms_id', 'status', 'total']
# sub_grid_area = pd.read_csv(r"ITRIcms_log60.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIcms_log60', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['radar_id', 'Timestamp', 'totalSpeed', 'motorSpeed', 'carSpeed', 'truckSpeed', 'totalVolume', 'carsVolume', 'motorVolume', 'truckVolume']
# sub_grid_area = pd.read_csv(r"ITRIradar.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIradar', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['radar_id', 'Timestamp', 'totalSpeed', 'motorSpeed', 'carSpeed', 'truckSpeed', 'totalVolume', 'carsVolume', 'motorVolume', 'truckVolume']
# sub_grid_area = pd.read_csv(r"ITRIradar05.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIradar05', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['radar_id', 'Timestamp', 'totalSpeed', 'motorSpeed', 'carSpeed', 'truckSpeed', 'totalVolume', 'carsVolume', 'motorVolume', 'truckVolume']
# sub_grid_area = pd.read_csv(r"ITRIradar15.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIradar15', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['radar_id', 'Timestamp', 'totalSpeed', 'motorSpeed', 'carSpeed', 'truckSpeed', 'totalVolume', 'carsVolume', 'motorVolume', 'truckVolume']
# sub_grid_area = pd.read_csv(r"ITRIradar60.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIradar60', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'heading', 'road_id', 'obu_id', 'stoptimes']
# sub_grid_area = pd.read_csv(r"ITRIstop.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIstop', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'hv_id', 'warning_state', 'total', 'road_id', 'heading']
# sub_grid_area = pd.read_csv(r"ITRIv2v.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIv2v', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'hv_id', 'warning_state', 'total', 'road_id', 'heading']
# sub_grid_area = pd.read_csv(r"ITRIv2v05.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIv2v05', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'hv_id', 'warning_state', 'total', 'road_id', 'heading']
# sub_grid_area = pd.read_csv(r"ITRIv2v15.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIv2v15', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['timestamp', 'hv_id', 'warning_state', 'total', 'road_id', 'heading']
# sub_grid_area = pd.read_csv(r"ITRIv2v60.csv", header=None, names=header)
# sub_grid_area.to_sql('ITRIv2v60', engine, if_exists='append', index=False, chunksize=500)
#
#
# header = ['RoadID', 'InfoDate', 'InfoHR', 'TotalDelay', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'LOSTotal', 'LOSD0', 'LOSD1', 'LOSD2', 'LOSD3', 'LOSD4', 'LOSD5', 'LOSD6', 'LOSD7']
# sub_grid_area = pd.read_csv(r"LOSData.csv", header=None, names=header)
# sub_grid_area.to_sql('LOSData', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'WeekdayType', 'PeakHourType', 'InfoHR']
# sub_grid_area = pd.read_csv(r"LOSPeakHour.csv", header=None, names=header)
# sub_grid_area.to_sql('LOSPeakHour', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'WeekdayType', 'InfoHR', 'Direction', 'GreenTime', 'CycleTime']
# sub_grid_area = pd.read_csv(r"LOSTODInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('LOSTODInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['LaneID', 'SegmentID', 'LaneName', 'LaneType', 'LaneCarType']
# sub_grid_area = pd.read_csv(r"LaneInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('LaneInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'Infodate', 'WeekdayType', 'TODType', 'TimeFrom', 'TimeTo', 'MaxPCU', 'PHF', 'P0', 'P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7', 'D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7']
# sub_grid_area = pd.read_csv(r"PeakHour.csv", header=None, names=header)
# sub_grid_area.to_sql('PeakHour', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'WeekdayType', 'TODType', 'TimeFrom', 'TimeTo']
# sub_grid_area = pd.read_csv(r"PeakHourInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('PeakHourInfo', engine, if_exists='append', index=False, chunksize=500)
#
#
# header = ['RoadID', 'RType', 'RoadFName', 'RoadSName']
# sub_grid_area = pd.read_csv(r"RoadInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('RoadInfo', engine, if_exists='append', index=False, chunksize=500)
#
#
#
# header = ['UniID', 'DeviceID', 'DetectID', 'RoadID', 'SegmentID', 'Direction', 'Threshold', 'ParkingType', 'Remark']
# sub_grid_area = pd.read_csv(r"SLDInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('SLDInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['Id', 'UniID', 'DeviceID', 'SegmentID', 'Direction', 'TurnID', 'CarID', 'CarType', 'Infotime',
#           'VideoStime', 'VideoEtime', 'IvideoName', 'LvideoName', 'IpictureName', 'LpictureName', 'IscreenshotTime',
#           'LscreenshotTime', 'LicenseID', 'Isvideo', 'Ispicture']
# sub_grid_area = pd.read_csv(r"STI.csv", header=None, names=header)
# sub_grid_area.to_sql('STI', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['UniID', 'DeviceID', 'SegmentID', 'Direction', 'TurnID', 'TurnType']
# sub_grid_area = pd.read_csv(r"STInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('STInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['SegmentID', 'RoadIDS', 'RoadIDE', 'SegmentName', 'Direction', 'Control']
# sub_grid_area = pd.read_csv(r"SegmentInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('SegmentInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['Signalid', 'Date', 'Workday', 'StartTime', 'EndTime', 'SubPhase', 'GreenTime', 'TimingPlan']
# sub_grid_area = pd.read_csv(r"SignalTOD.csv", header=None, names=header)
# sub_grid_area.to_sql('SignalTOD', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['Singal_id', 'TimingPlan', 'PhaseId', 'SubPhase', 'NextSubPhase', 'NextGreen', 'DateTime', 'SignalType', 'RemainSec']
# sub_grid_area = pd.read_csv(r"Signal_log.csv", header=None, names=header)
# sub_grid_area.to_sql('Signal_log', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'TODType', 'TimeFrom', 'TimeTo']
# sub_grid_area = pd.read_csv(r"TODInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('TODInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'RoadName', 'Direction', 'TurnID', 'TotalV', 'PCU', 'DirV', 'DirP', 'InfoTime', 'Pedestrian',
#           'Obstacle', 'Bicycle', 'Motorcycle', 'Car', 'MotorBus', 'PickupTruck', 'Taxi', 'MicroBus', 'TourBus',
#           'MotorTruck', 'TankTruck', 'FullTrailer', 'Trailer', 'Dump', 'Tractor', 'ConcreteTruck', 'FireEngine',
#           'GarbageTruck', 'Grane', 'Stacker']
# sub_grid_area = pd.read_csv(r"TurnData.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnData', engine, if_exists='append', index=False, chunksize=500)
#
# sub_grid_area = pd.read_csv(r"TurnData05.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnData05', engine, if_exists='append', index=False, chunksize=500)
#
# sub_grid_area = pd.read_csv(r"TurnData15.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnData15', engine, if_exists='append', index=False, chunksize=500)
#
# sub_grid_area = pd.read_csv(r"TurnData60.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnData60', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['DeviceID', 'Direction', 'TurnID', 'CarID', 'CarType', 'Stime', 'Etime']
# sub_grid_area = pd.read_csv(r"TurnDataDynamic.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnDataDynamic', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['RoadID', 'RoadName', 'Direction', 'TurnID', 'TotalV', 'PCU', 'DirV', 'DirP', 'InfoTime', 'Pedestrian',
#           'Obstacle', 'Bicycle', 'Motorcycle', 'Car', 'MotorBus', 'PickupTruck', 'Taxi', 'MicroBus', 'TourBus',
#           'MotorTruck', 'TankTruck', 'FullTrailer', 'Trailer', 'Dump', 'Tractor', 'ConcreteTruck', 'FireEngine',
#           'GarbageTruck', 'Grane', 'Stacker']
# sub_grid_area = pd.read_csv(r"TurnDataday.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnDataday', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['Uid', 'DeviceID', 'SegmentID', 'Direction', 'TurnID', 'DetectFrom', 'DetectTo', 'DetectMid', 'TurnC']
# sub_grid_area = pd.read_csv(r"TurnInfo.csv", header=None, names=header)
# sub_grid_area.to_sql('TurnInfo', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['id', 'InfoDate', 'Weather']
# sub_grid_area = pd.read_csv(r"WeatherKaohsiung.csv", header=None, names=header)
# sub_grid_area.to_sql('WeatherKaohsiung', engine, if_exists='append', index=False, chunksize=500)
#
# header = ['id', 'user_email', 'password', 'is_active', 'user_type']
# sub_grid_area = pd.read_csv(r"web_users.csv", header=None, names=header)
# sub_grid_area.to_sql('web_users', engine, if_exists='append', index=False, chunksize=500)
