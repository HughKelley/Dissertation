# -*- coding: utf-8 -*-
#!/usr/bin/python
"""
Created on Thu Jul 11 14:27:23 2019

@author: Hugh
"""

from config import config
 
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
      
        # create a cursor
        cur = conn.cursor()
        
   # execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
 
        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)
       
       # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    connect()





# import req modules
import pandas as pd
import psycopg2

import numpy as np

# connect to postgres

conn = psycopg2.connect("dbname=Dissertation user=postgres password=tuesday789")

# test select statement

# grab data to upload

# test upload