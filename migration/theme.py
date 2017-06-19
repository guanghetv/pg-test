# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2


# pymongo
mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
themes = db['themes']

# psycopg2
conn = psycopg2.connect("""
    password=Yangcong345
    host=10.8.8.8
    port=5432
    dbname=postgres
    user=postgres""")

# conn = psycopg2.connect("""
#     password=Yangcong345
#     host=onion345.pg.rds.aliyuncs.com
#     port=3432
#     dbname=onion
#     user=onions""")

with conn.cursor() as cur:
    for theme in themes.find():

        sql = """
            INSERT INTO theme (
                "chapterId",
                "name",
                "pay",
                "state",
                "icons",
                "relatedThemeId",
                "hasPainPoint",
                "hasKeyPoint",
                "coverImage",
                "description",
                _id)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,ARRAY[%s],%s,%s)"""

        try:
            # tranform
            if ('desc' in theme and 'images' in theme['desc']):
                coverImage = theme['desc']['images']
                if not coverImage:
                    coverImage = None
            else:
                coverImage = None

            # if (coverImage is not None):
                # for image in coverImage:
                #     'ARRAY[]'.format()

            # print 'coverImage: ', coverImage

            # desc.text
            if ('desc' in theme and 'text' in theme['desc']):
                text = theme['desc']['text']
                if not text:
                    text = None
            else:
                text = None

            # INSERT
            sql = cur.mogrify(sql, (
                '87281f30-51a3-11e7-8034-833af1d88564', # 稍后需要更新
                theme['name'],
                theme['pay'] if ('pay' in theme) else None,
                'published', # 暂时都填充已发布
                # theme['icons'],
                None,
                str(theme['related']) if ('related' in theme) else None,
                theme['hasPainPoint'] if ('hasPainPoint' in theme) else None,
                theme['hasKeyPoint'] if ('hasKeyPoint' in theme) else None,
                'xxx',
                text,
                None))

            cur.execute(sql)
            conn.commit()
        except Exception as e:
            print sql

            print 'error: ', e
            conn.rollback()

            raise e

conn.close()