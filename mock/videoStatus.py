# from pymongo import MongoClient
import psycopg2
import os
import re

conn = psycopg2.connect("host=10.8.2.42 password=198325 dbname=onion user=postgres")
pg = conn.cursor()

pg.execute('select * from video limit 2;')
for row in pg:
    print row
