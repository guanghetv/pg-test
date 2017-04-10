# -*- coding: UTF-8 -*-

# from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import os
import re
import time
import multiprocessing

dbUser = 'master'
host = 'onion-t04.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'
userCount = 20000

conn = psycopg2.connect("host={} password=Yangcong345 dbname=onion user={}".format(host, dbUser))
dictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

dictCursor.execute("""SELECT id from "user" limit {}; """.format(userCount))
userIds = dictCursor.fetchall()

# flatten
userIds = [val for sublist in userIds for val in sublist]

dictCursor.close()
conn.close()

print 'userIds count: ', len(userIds)

# mock data
def mock(start, end):
    # conn
    conn = psycopg2.connect("host={} password=Yangcong345 dbname=onion user={}".format(host, dbUser))
    dictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # slice
    ids = userIds[start:end]
    print 'start, end ', start, end

    for userId in ids:
        sql = """
            SELECT id, name, phone from "userLocal" where id = %s; """

        try:
            _sql = dictCursor.mogrify(sql, (userId,))
            dictCursor.execute(_sql)

            # print dictCursor.fetchone()
            # conn.commit()
        except Exception as e:
            print 'error: ', e
            # conn.rollback()

    dictCursor.close()
    conn.close()

    print 'finish: start ', start


# mock(0, 3)

# multiprocessing
beginTime = time.time()
LIMIT = 20
start = 0
CPU_COUNT = userCount / LIMIT

pool = multiprocessing.Pool(processes=CPU_COUNT)
for i in range(CPU_COUNT):
    end = start + LIMIT
    pool.apply_async(mock, (start, end, ))
    start = end

pool.close()
pool.join()

# all finished
endTime = time.time()
print 'all take time: ', endTime - beginTime
