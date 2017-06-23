# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import psycopg2.extras
from bson.objectid import ObjectId

# pymongo
mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
topics = db['topics']
hypervideos = db['hypervideos']

# psycopg2
conn = psycopg2.connect("""
    password=Yangcong345
    host=10.8.8.8
    port=5432
    dbname=test
    user=postgres""")


###
counter = 0

with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    cur.execute('select * from topic')
    for pgTopic in cur:
        # print ObjectId(topic['_id'])

        topic = topics.find_one({'_id': ObjectId(pgTopic['_id'])})
        if (topic['hyperVideo'] and topic['subject'] == 'math'):
            # print 'aa ', topic

            # find video
            video = None
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur1:
                cur1.execute('select * from video where _id = %s', (str(topic['hyperVideo']),))
                video = cur1.fetchone()

            # insert
            with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur2:
                print 'xx ', pgTopic['id']
                # print 'xx ', video['id']

                # 特例
                _videoId = '75494866-555e-11e7-8c66-2bd4ab5af499' if (str(pgTopic['id']) == 'f314339e-565a-11e7-90bf-e7a7d9f31ffa') else video['id']

                cur2.execute('insert into "topicVideo" ("topicId", "videoId") values (%s, %s)',
                    (pgTopic['id'], _videoId))
                    # (pgTopic['id'], video['id']))
                conn.commit()
                counter += 1
                print counter

            # try:
            #     cur.execute(sql)
            #     conn.commit()

            # except Exception as e:
            #     print sql
            #     # print theme
            #     print topic

            #     print 'error: ', e
            #     conn.rollback()

            #     exit()
            #     raise e
        

conn.close()

