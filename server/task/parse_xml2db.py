import pandas as pd
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

cfg = json.load(open('config.json', 'r'))
Base = declarative_base()
engine = create_engine(cfg['db'], echo=True)
DB_session = sessionmaker(engine)
db_session = DB_session()
Base.metadata.create_all(engine)

# BusICTicket_df = pd.read_xml('bus_tickets_data/202105_ic_KHH_0901_03.xml', parser='etree', xpath='.//BusICTickets//BusICTicket')
# ODFareRide_df = pd.read_xml('bus_tickets_data/202105_ic_KHH_0901_03.xml', parser='etree', xpath='.//BusICTickets//BusICTicket//ODFareRide')
# BusICTicket_df = BusICTicket_df.join(ODFareRide_df)
# BusICTicket_df.to_sql('bus_ic_tickets', engine, if_exists='append', index=False, chunksize=500, )
# print(BusICTicket_df)


res = requests.get('https://kpp.tbkc.gov.tw/parking/V1/parking/OffStreet/CarPark/Availability')
xml_str = res.content.decode('utf-8')
xml_str = xml_str[xml_str.find('<'):]
parking_df = pd.read_xml(xml_str, xpath='//abc:ParkingAvailability', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})
parking_df = pd.read_xml(xml_str, xpath='//abc:ParkingAvailability', namespaces={'abc': "https://traffic.transportdata.tw/standard/parking/schema/"})
print(parking_df)
