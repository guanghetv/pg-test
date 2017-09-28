# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import os
import re
import traceback
from datetime import datetime, timedelta
from pytz import timezone, utc
import time
import multiprocessing


def run (skip, limit):
    beginTime = time.time()

    # pymongo
    mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
    db = mongo['onions4']
    topicprogresses = db['topicprogresses']

    # psycopg2
    conn_course = psycopg2.connect("""
        password=Yangcong345
        host=10.8.8.8
        port=5432
        dbname=course
        user=postgres""")

    conn_mydb = psycopg2.connect("""
        password=unitedmaster
        host=10.8.8.101
        port=5432
        dbname=mydb
        user=postgres""")


    # video map
    videoMap = {}
    with conn_course.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(""" SELECT * FROM video """)
        for video in cur:
            # print video['id']
            videoMap[video['_id']] = video

    problemMap = {}
    with conn_course.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
        cur.execute(""" SELECT problem.*, goal."subjectId", goal."stageId" FROM problem JOIN goal ON goal.id = problem."goalId" """)
        for problem in cur:
            # print video['id']
            problemMap[problem['_id']] = problem

    conn_course.close()

    # print problemMap


    # counter = 0

    with conn_mydb.cursor() as cur:
        myProgress = topicprogresses.find().skip(skip*limit).limit(limit)
        print 'fork: skip from %d, limit %d' % (skip*limit, limit)

        for topicprogress in myProgress:
            # print topicprogress

            # counter = counter + 1
            # if (counter >= 100000):
            #     exit()


            # print topicprogress

            if ('_id' not in topicprogress['video']):
                print 'lack of video id', topicprogress['_id']
                continue

            oldVideoId = str(topicprogress['video']['_id'])
            userId = str(topicprogress['userId'])

            for problem in topicprogress['practice']['problems']:
                try:
                    oldProblemID = str(problem['_id'])
                    if (oldProblemID not in problemMap):
                        print 'the problem not exists in pg'
                        continue

                    # str(problem['time'].split('.')[0]
                    mytime = datetime.strptime(str(problem['time']).split('.')[0], "%Y-%m-%d %H:%M:%S")
                    mytime += timedelta(hours=8)

                    sql = cur.mogrify("""
                        INSERT INTO problem_log (
                            "userId",
                            "videoId",
                            "problemId",
                            "subjectId",
                            "stageId",
                            duration,
                            level,
                            answers,
                            correct,
                            "submitTime",
                            type
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                        (
                            userId,
                            videoMap[oldVideoId]['id'],
                            problemMap[oldProblemID]['id'],
                            problemMap[oldProblemID]['subjectId'],
                            problemMap[oldProblemID]['stageId'],
                            problem['duration'] if ('duration' in problem) else None,
                            problem['levelNo'],
                            problem['answers'],
                            # problem['answers'].encode('utf-8'),
                            problem['correct'],
                            mytime,
                            problemMap[oldProblemID]['type']
                        ))

                    # print 'sql', sql

                    cur.execute(sql)
                    conn_mydb.commit()

                    # exit()
                except Exception as e:
                    print sql
                    print 'problem ', problem

                    traceback.print_exc()
                    conn_mydb.rollback()

                    exit()

    conn_mydb.close()

    endTime = time.time()
    print 'take time: ', endTime - beginTime


# fork

total_count = 51762006
CPU_COUNT = 200
LIMIT = total_count/CPU_COUNT


# # multiprocessing
pool = multiprocessing.Pool(processes=CPU_COUNT)
for i in range(CPU_COUNT+1):
    pool.apply_async(run, (i, LIMIT, ))

pool.close()
pool.join()





