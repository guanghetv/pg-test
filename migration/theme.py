# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import psycopg2.extras

# pymongo
mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
themes = db['themes']
chapters = db['chapters']

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

with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
    for chapter in chapters.find({'status': 'published'}):
        themeIds = chapter['themes']

        # 通过发布的章节找主题，避免无效的主题数据
        for theme in themes.find({'_id': {'$in': themeIds}, 'type': {'$ne': 'exam'}}):
            sql = None

            try:
                # chapterId
                pgChapter = cur.execute('select * from chapter where _id = %s;',
                    (str(chapter['_id']),))

                pgChapter = cur.fetchone()

                # tranform
                coverImages = None
                if ('desc' in theme and 'images' in theme['desc']):
                    coverImages = theme['desc']['images']

                _coverImages = None
                if (coverImages is not None and (len(coverImages) > 0)):
                    _coverImages = "{"+ coverImages[0] +"}"

                # desc.text
                if ('desc' in theme and 'text' in theme['desc']):
                    text = theme['desc']['text']
                    if not text:
                        text = None
                else:
                    text = None

                # theme_icon[]
                icon0 = theme['icons'][0]
                icon1 = theme['icons'][1]

                i1 = '("{0}",{1},{2})'.format(
                    icon0['pic'],
                    icon0['background'],
                    'common'
                )

                i2 = '("{0}",{1},{2})'.format(
                    icon1['pic'],
                    icon1['background'],
                    'perfect'
                )

                # INSERT
                sql = cur.mogrify("""
                    INSERT INTO theme (
                        "chapterId",
                        "name",
                        "pay",
                        "state",
                        "icons",
                        "relatedThemeId",
                        "related",
                        "hasPainPoint",
                        "hasKeyPoint",
                        "coverImages",
                        "description",
                        _id)
                    VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        ARRAY[%s, %s]::theme_icon[],
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    )
                    """,
                    (
                        pgChapter['id'],
                        theme['name'],
                        theme['pay'] if ('pay' in theme) else False,
                        'published', # 暂时都填充已发布
                        i1,
                        i2,
                        None, # 稍后更新 relatedThemeId
                        str(theme['related']) if ('related' in theme) else None,
                        theme['hasPainPoint'] if ('hasPainPoint' in theme) else False,
                        theme['hasKeyPoint'] if ('hasKeyPoint' in theme) else False,
                        _coverImages,
                        text,
                        str(theme['_id'])))

                # print sql
                # exit()

                cur.execute(sql)
                conn.commit()
            except Exception as e:
                print sql
                print chapter
                print theme

                print 'error: ', e
                conn.rollback()

                exit()
                # raise e

conn.close()