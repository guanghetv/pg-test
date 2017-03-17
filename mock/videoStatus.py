# from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import os
import re
import time
import multiprocessing

dbUser = 'master'
host = 'onions-test0314.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'

# dbUser = 'postgres'
# host = '10.8.2.42'

conn = psycopg2.connect("host={} password=Yangcong345 dbname=onion user={}".format(host, dbUser))
dictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# video map
dictCursor.execute('select * from video;')
videos = dictCursor.fetchall()
dictCursor.close()
conn.close()

print 'video count: ', len(videos)

# mock data
def mock(limit, offset):
    # conn
    conn = psycopg2.connect("host={} password=Yangcong345 dbname=onion user={}".format(host, dbUser))
    dictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # user
    dictCursor.execute('select * from "user" LIMIT {} OFFSET {};'.format(limit, offset))

    print 'limit, offset ', limit, offset

    for row in dictCursor:
        userId = row['id']

        with conn.cursor() as videoStatusCur:
            print 'conn..'

            for video in videos:
                videoId = video['id']
                sql = """
                    INSERT INTO "videoStatus" ("userId","videoId","finishTime",state) \
                    VALUES (%s, %s, %s, %s) """

                print 'pre insert'
                videoStatusCur.execute(sql, (userId, videoId, None, 'unfinished'))
                print 'insert'

            conn.commit()
            print 'commit'

    dictCursor.close()
    conn.close()


# mock(1, 0)

# multiprocessing
beginTime = time.time()
CPU_COUNT = 2
LIMIT = 1

pool = multiprocessing.Pool(processes=CPU_COUNT)
for i in range(CPU_COUNT+1):
    offset = i*LIMIT
    pool.apply_async(mock, (LIMIT, offset, ))

pool.close()
pool.join()

# all finished
endTime = time.time()
print 'all take time: ', endTime - beginTime
