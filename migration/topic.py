# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import psycopg2.extras

# pymongo
mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
themes = db['themes']
topics = db['topics']
# chapters = db['chapters']

# psycopg2
conn = psycopg2.connect("""
    password=Yangcong345
    host=10.8.8.8
    port=5432
    dbname=postgres
    user=postgres""")


###
counter = 0

with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    for theme in themes.find():
        if ('topics' not in theme):
            continue

        topicIds = theme['topics']

        # check theme is valid
        themeId = None
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur1:
            cur1.execute('select * from theme where _id = %s', (str(theme['_id']),))
            pgTheme = cur1.fetchone()
            if (pgTheme is None):
                print 'invalid theme'
                continue
            else:
                themeId = str(pgTheme['id'])

        # topic
        for topic in topics.find({
            '_id': {'$in': topicIds},
            'type': {'$nin': ['jyfs','dtsz','chapter_exam']},
            'subject': {'$ne': 'physics'}}):
            # print topic

            sql = cur.mogrify("""INSERT INTO topic (
                "themeId",
                "name",
                "pay",
                "type",
                "state",
                "keyPoint",
                "painPoint",
                "coverImage",
                "description",
                _id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (
                themeId,
                topic['name'],
                topic['pay'] if ('pay' in topic) else False,
                topic['type'],
                'published',
                topic['keyPoint'] if ('keyPoint' in topic) else False,
                topic['painPoint'] if ('painPoint' in topic) else None,
                topic['coverPic'] if ('coverPic' in topic) else None,
                topic['desc'] if ('desc' in topic) else None,
                str(topic['_id'])))

            # print sql
            # exit()
            try:

                cur.execute(sql)
                conn.commit()

                counter += 1
                print counter
            except Exception as e:
                print sql
                # print theme
                print topic

                print 'error: ', e
                conn.rollback()

                exit()
                # raise e

conn.close()

