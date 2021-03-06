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

# dbUser = 'postgres'
# host = '10.8.2.42'

conn = psycopg2.connect("host={} password=Yangcong345 dbname=onion user={}".format(host, dbUser))
dictCursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# video map, exclude 初中物理
dictCursor.execute("""
    SELECT * from video v
        where not exists
        (select * from video v1 where v.subject = 'physics' and v.stage = 'middle');
    """)
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
    dictCursor.execute('SELECT * from "user" order by id asc OFFSET {} LIMIT {};'.format(offset, limit))

    print 'limit, offset ', limit, offset

    for row in dictCursor:
        userId = row['id']

        with conn.cursor() as videoStatusCur:

            # TODO: 需要把用户完成视频的记录打散，更加随机
            for video in videos:
                videoId = video['id']
                subject = video['subject']
                stage = video['stage']

                sql = """
                    UPDATE "videoStatusMathHigh" set state = 'finished', "finishTime" = now()
                    where "userId" = (%s) and "videoId" = (%s) """

                try:
                    videoStatusCur.execute(sql, (userId, videoId))
                    conn.commit()
                except Exception as e:
                    print 'error: ', e
                    conn.rollback()
                    # break
                    # raise e

    dictCursor.close()
    conn.close()

    print 'finish: offset ', offset


# multiprocessing
beginTime = time.time()
CPU_COUNT = 10
LIMIT = 1

pool = multiprocessing.Pool(processes=CPU_COUNT)
for i in range(CPU_COUNT):
    offset = i*LIMIT
    pool.apply_async(mock, (LIMIT, offset, ))

pool.close()
pool.join()

# all finished
endTime = time.time()
print 'all take time: ', endTime - beginTime
