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


mrt_trans_count_df = pd.read_csv('mrt_data/mrt_data.csv')
mrt_trans_count_df.to_sql('mrt_trans_count', engine, if_exists='append', index=False, chunksize=500, )
# print(BusICTicket_df)

