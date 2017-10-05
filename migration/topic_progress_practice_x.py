# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import psycopg2.extras
import os
import re
import sys
import traceback
from datetime import datetime, timedelta
import time
import multiprocessing
from time import sleep
from bson import ObjectId


# TODO: clean 重复提交做题数据

def run (skip, limit):

    try:
        beginTime = time.time()

        # pymongo
        mongo = MongoClient(host='10.8.8.12', port=27017, connect=True)
        db = mongo['onions-0926']
        users = db['users']
        topicprogresses = db['topicprogresses']

        # psycopg2
        conn_course = psycopg2.connect("""
            password=Yangcong345
            host=10.8.8.8
            port=5432
            dbname=course
            user=postgres""")

        conn_study = psycopg2.connect("""
            password=unitedmaster
            host=10.8.8.101
            port=5432
            dbname=study_x
            user=postgres""")

        # video map
        videoMap = {}
        with conn_course.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(""" SELECT * FROM video """)
            for video in cur:
                videoMap[video['_id']] = video

        problemMap = {}
        new_problem_map = {}
        with conn_course.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(""" SELECT problem.*, goal."subjectId", goal."stageId" FROM problem JOIN goal ON goal.id = problem."goalId" """)
            for problem in cur:
                # print video['id']
                problemMap[problem['_id']] = problem
                new_problem_map[problem['id']] = problem

        conn_course.close()

        # print problemMap


        counter = 0

        with conn_study.cursor() as cur:
            # user_cur = users.find({"_id" : ObjectId("59a8d046d055b307305cd350")})
            user_cur = users.find({}, no_cursor_timeout=True).skip(skip*limit).limit(limit)
            print 'fork: skip from %d, limit %d' % (skip*limit, limit)
            # sleep(6)

            for user in user_cur:
                #
                # counter = counter + 1
                # if (counter % 10000 == 0): # reduce stdout
                #     print 'counter: ', counter
                #     print time.time() - beginTime

                myProgress = topicprogresses.find({"userId" : user['_id']}, no_cursor_timeout=True)

                # myProgress = topicprogresses.find().skip(skip*limit).limit(limit)


                tup = []
                for topicprogress in myProgress:
                    try:
                        if ('_id' not in topicprogress['video'] and len(topicprogress['video']['records']) == 0):
                            # print 'lack of video id', topicprogress['_id']
                            continue

                        oldVideoId = str(topicprogress['video']['_id'])
                        userId = str(topicprogress['userId'])

                        # tup = []
                        for problem in topicprogress['practice']['problems']:

                            oldProblemID = str(problem['_id'])
                            if (oldProblemID not in problemMap and (oldProblemID not in new_problem_map)):
                                # print 'the problem not exists in pg'
                                continue

                            #
                            try:
                                mytime = datetime.strptime(str(problem['time']).split('.')[0], "%Y-%m-%d %H:%M:%S")
                                mytime += timedelta(hours=8)
                            # '13794-04-06 01:25:12' does not match format '%Y-%m-%d %H:%M:%S'
                            except ValueError as e:
                                traceback.print_exc()
                                continue

                            if ('serverTime' in problem):
                                server_time = datetime.strptime(str(problem['serverTime']), "%Y-%m-%d %H:%M:%S.%f")
                                server_time = timedelta(hours=8)
                            else:
                                server_time = mytime
                            ##
                            try:
                                _tuple = (
                                    userId,
                                    videoMap[oldVideoId]['id'] if (oldVideoId in videoMap) else oldVideoId,
                                    problemMap[oldProblemID]['id'] if (oldProblemID in problemMap) else oldProblemID,
                                    problemMap[oldProblemID]['subjectId'],
                                    problemMap[oldProblemID]['stageId'],
                                    problem['duration'] if ('duration' in problem) else None,
                                    # problem['levelNo'],
                                    problem['answers'],
                                    # problem['answers'].encode('utf-8'),
                                    problem['correct'],
                                    mytime,
                                    problemMap[oldProblemID]['type'],
                                    server_time
                                )
                                sql = cur.mogrify('(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', _tuple)
                                tup.append(sql)
                            except ValueError as e: # contain NUL (0x00) characters
                                print '_tuple ', _tuple
                                traceback.print_exc()
                                continue


                            # tup.append((
                            #     userId,
                            #     videoMap[oldVideoId]['id'] if (oldVideoId in videoMap) else oldVideoId,
                            #     problemMap[oldProblemID]['id'] if (oldProblemID in problemMap) else oldProblemID,
                            #     problemMap[oldProblemID]['subjectId'],
                            #     problemMap[oldProblemID]['stageId'],
                            #     problem['duration'] if ('duration' in problem) else None,
                            #     # problem['levelNo'],
                            #     problem['answers'],
                            #     # problem['answers'].encode('utf-8'),
                            #     problem['correct'],
                            #     mytime,
                            #     problemMap[oldProblemID]['type']
                            # ))

                    except Exception as e:
                        traceback.print_exc()
                        raise e

                myProgress.close()


                # compose
                if (len(tup) == 0):
                    # print 'tup null'
                    continue

                args_str = ','.join(x for x in tup)
                # args_str = ','.join(cur.mogrify('(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', x) for x in tup)
                # print 'args_str ', args_str

                try:
                    cur.execute("""
                        INSERT INTO problem_log (
                            "userId",
                            "videoId",
                            "problemId",
                            "subjectId",
                            "stageId",
                            duration,
                            -- level,
                            answers,
                            correct,
                            "submitTime",
                            type,
                            "createTime"
                        ) VALUES """ + args_str)
                    conn_study.commit()
                except Exception as e:
                    print 'args_str ', args_str
                    traceback.print_exc()
                    conn_study.rollback()
                    raise e


            user_cur.close()


        conn_study.close()

        endTime = time.time()
        print 'take time: ', endTime - beginTime

    except Exception as e:
        traceback.print_exc()
        raise e

    


# fork

try:
    total_count = 9272721
    CPU_COUNT = 30
    LIMIT = total_count/CPU_COUNT


    # # multiprocessing
    pool = multiprocessing.Pool(processes=CPU_COUNT)
    for i in range(CPU_COUNT+1):
        pool.apply_async(run, (i, LIMIT, ))

    pool.close()
    pool.join()

except Exception as e:
    traceback.print_exc()
    raise e


# run(0, 7)





