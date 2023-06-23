#!/usr/bin/env python
# coding: utf-8

# In[9]:

import argparse
import os
import pandas as pd
from sqlalchemy import create_engine

from time import time
import pyarrow.parquet as pq

def main(params) : 
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    url = params.url
    table_name = params.table_name

    parq_name = 'output.parquet'
    print("URL : ",url)
    os.system(f"wget {url} -O {parq_name}")

    engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db}')
    engine.connect()
    #engine = f"postgresql://{user}:{password}@{host}:{port}/{db}"
    print("HOST : ",host,' ',port)
    parquet_file = pq.ParquetFile(parq_name)
    for i in parquet_file.iter_batches():
        t_start = time()

        pd_i = i.to_pandas()
        pd_i.to_sql(name=table_name,con=engine,if_exists='append')
        
        t_end = time()
        print("Batch sent in : ",t_end - t_start)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description="Ingest CSV data into Postgres")
    #User, pwd, host, port db name, table name, url of the csv

    parser.add_argument('--user',help='User Name for postgres')
    parser.add_argument('--password',help='Password for postgres')
    parser.add_argument('--host',help='Host for postgres')
    parser.add_argument('--port',help='Port for postgres')
    parser.add_argument('--db',help='db for postgres')
    parser.add_argument('--url',help="Url for the data")
    parser.add_argument('--table_name',help='Table Name in postgres')

    args = parser.parse_args()
    main(args)
