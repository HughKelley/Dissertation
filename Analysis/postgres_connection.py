# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 14:39:34 2019

@author: Hugh
"""

import psycopg2

conn = psycopg2.connect(database="Dissertation", user="postgres", password="tuesday789")

cur = conn.cursor()

cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")

cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",(100, "abc'def"))

cur.execute("SELECT * FROM test;")

cur.fetchone()


conn.commit()

cur.close()

conn.close()


# works like a charm. Created test table successfully 
# double checked in pgAdmin