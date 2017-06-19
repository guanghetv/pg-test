# -*- coding: utf-8 -*-

from pymongo import MongoClient
import psycopg2
import os
import re

# enum
publisherMap = {
    '人教版': 1,
    '北师大版': 2,
    '华师大版': 3,
    '湘教版': 4,
    '冀教版': 5,
    '苏科版': 6,
    '鲁教版': 7,
    '沪科版': 8,
    '沪教版': 9,
    '青岛版': 10,
    '浙教版': 11,
    '北京课改版': 12,
    '通用版': 13
}

semesterMap = {
    '一年级上': 1,
    '一年级下': 2,
    '二年级上': 3,
    '二年级下': 4,
    '三年级上': 5,
    '三年级下': 6,
    '四年级上': 7,
    '四年级下': 8,
    '五年级上': 9,
    '五年级下': 10,
    '六年级上': 11,
    '六年级下': 12,
    '七年级上': 13,
    '七年级下': 14,
    '八年级上': 15,
    '八年级下': 16,
    '九年级上': 17,
    '九年级下': 18,
    '高一上': 19,
    '高一下': 20,
    '高二上': 21,
    '高二下': 22,
    '高三上': 23,
    '高三下': 24
}

subjectMap = {
    'math': 1,
    'physics': 2,
}

# pymongo
mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
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


###
filename = 'data/chapters.csv'

with conn.cursor() as cur:
    for chapter in chapters.find({'status': 'published'}):
        sql = """
            INSERT INTO chapter (
                "publisherId",
                "semesterId",
                "subjectId",
                "stageId",
                name,
                "state",
                "order",
                "includePay"
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

        try:
            cur.execute(sql,
                (publisherMap[chapter['publisher'].encode("utf-8")],
                    semesterMap[chapter['semester'].encode("utf-8")],
                    subjectMap[chapter['subject'].encode("utf-8")],
                    2,
                    chapter['name'],
                    chapter['status'],
                    chapter['order'],
                    chapter['includeCharges']))

            conn.commit()
        except Exception as e:
            print 'error: ', e
            conn.rollback()

            raise e

conn.close()

    

    # with open(filename, 'a') as file:
    #     file.write(dumps(chapter))

# chapters
# os.system("""mongoexport -h 10.8.8.8 -d onions4 -c chapters \
#     --fields subject,name,status,order,createTime,_id \
#     --type=csv -o data/chapters.csv""")

# replace
# filename = "data/chapters.csv"
# with open(filename, 'r') as file:
#     result = re.sub(r'ObjectId\((.*?)\)', '\\1', file.read())
# with open(filename, 'w') as f:
#     f.write(result)

# currentDir = os.path.dirname(os.path.realpath(__file__))
# parentDir = os.path.dirname(currentDir)
# host = 'onions-test0314.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'
# cmd = """
#     PGPASSWORD=Yangcong345 \
#     psql -h {} -p 5432 \
#     -U master -d mydb \
#     -c "\copy chapter(subject,name,status,\\"order\\",\\"createTime\\",_id) \
#     from '{}/data/chapters.csv' \
#     delimiter as ',' csv header"
# """.format(host, parentDir)

# os.system(cmd)
