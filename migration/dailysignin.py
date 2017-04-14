from pymongo import MongoClient
# import psycopg2
import os
import re
import subprocess

mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
dailysignins = db['dailysignins']

currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.dirname(currentDir)

# dailysignins
if (os.path.isfile(parentDir +'/data/dailysignins.csv') == False):
    os.system("""
        ssh -n master@10.8.8.8 "mongoexport -h 10.8.8.8 -d onion40-0413 -c dailysignins --fields userId,level,nickname,channel,school,customSchool,aim,name,type,from,role,email,phone,coins,points,scores,region,nation,gender,province,semester,publisher,registTime,weekScores,activateDate,verifiedByPhone,vipExpirationTime,qqOpenId,createTime,learningTime,clientType,clientVersion,deviceId,userAgent,signInDate,year,month,day,hour,weekday,week --type=csv -o data/dailysignins.csv"
    """)

    print 'mongoexport finished'

    # scp
    os.system("""
        scp master@10.8.8.8:~/data/dailysignins.csv {}/data
        """.format(parentDir))

    print 'scp finished'

    # replace
    filename = "data/dailysignins.csv"
    with open(filename, 'r') as file:
        result = re.sub(r'ObjectId\((.*?)\)', '\\1', file.read())
    with open(filename, 'w') as f:
        f.write(result)

    print 'remove ObjectId tag finished'


# host = '10.8.2.42'
# dbUser = 'postgres'

# dbUser = 'master'
# host = 'onion-t02.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'

# cmd = """
#     PGPASSWORD=Yangcong345 \
#     psql -h {} -p 5432 \
#     -U {} -d onion \
#     -c "\copy \\"user\\"(name,target,\\"customSchool\\",nickname,password, \
#     channel,coins,points,type,gender,email,phone,\\"registTime\\",\\"from\\",role,salt,_id) \
#     from '{}/data/dailysignins.csv' \
#     delimiter as ',' csv header"
# """.format(host, dbUser, parentDir)

# print cmd

# os.system(cmd)
