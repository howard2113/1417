#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import time
import tempfile
import pandas as pd
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
file_transaction = 0


def mysql2csv(query, header, db_engine):  # for mysql
    start_t = time.time()
    global file_transaction
    default_path = f'D:/MySQL/Uploads/pd_temp{file_transaction}.csv'
    file_transaction += 1
    if file_transaction > 100:
        file_transaction = 0
    if os.path.isfile(default_path):
        os.remove(default_path)
    print('mysql2csv', time.time()-start_t, file_transaction)
    with db_engine.connect() as con:
        con.execute(f'''{query} INTO OUTFILE '{default_path}' FIELDS TERMINATED BY ',' ENCLOSED BY '' LINES TERMINATED BY '\\n';''')
        print('mysql2csv', time.time() - start_t, file_transaction)
        df = pd.read_csv(default_path, header=None, names=header)
        print('mysql2csv', time.time() - start_t, file_transaction)
        return df


def read_sql_tmpfile(query, db_engine):  # for postgresql
    with tempfile.TemporaryFile() as tmpfile:
        copy_sql = "COPY ({query}) TO STDOUT WITH CSV {head}".format(query=query, head="HEADER")
        conn = db_engine.raw_connection()
        cur = conn.cursor()
        cur.copy_expert(copy_sql, tmpfile)
        tmpfile.seek(0)
        df = pd.read_csv(tmpfile)
        return df
