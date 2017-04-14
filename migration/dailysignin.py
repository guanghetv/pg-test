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
        ssh -n master@10.8.8.8 "mongoexport -h 10.8.8.8 -d onion40-0413 -c dailysignins --fields userId,level,nickname,channel,school,customSchool,aim,name,type,from,role,email,phone,coins,points,scores,region,nation,gender,province,semester,publisher,registTime,weekScores,activateDate,verifiedByPhone,vipExpirationTime,qqOpenId,createTime,clientType,clientVersion,deviceId,userAgent,signInDate,year,month,day,hour,weekday,week --type=csv -o data/dailysignins.csv" with (delimiter '|')
    """)

    print 'mongoexport finished'

    # scp
    os.system("""
        scp master@10.8.8.8:~/data/dailysignins.csv {}/data
        """.format(parentDir))

    print 'scp finished'

    # wirte file
    wFile = open('data/dailysignins_new.csv', 'a')

    # replace
    filename = "data/dailysignins_t.csv"
    with open(filename, 'r') as file:
        for line in file:
            #convert objectId
            result = re.sub(r'ObjectId\((.*?)\)', '\\1', line)

            # append into file
            wFile.write(result)

    wFile.close()

    print 'convert format finished'


# host = '10.8.2.42'
# dbUser = 'postgres'

dbUser = 'master'
host = 'onion-t02.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'

cmd = """
    PGPASSWORD=Yangcong345 \
    psql -h {} -p 5432 \
    -U {} -d onion \
    -c "\copy \\"dailySignin\\"(\\"userId\\",level,nickname,channel,school,\\"customSchool\\",
        aim,name,type,\\"from\\",role,email,phone,coins,points,scores,region,nation,gender,province,
        semester,publisher,\\"registTime\\",\\"weekScores\\",\\"activateDate\\",\\"verifiedByPhone\\",
        \\"vipExpirationTime\\",\\"qqOpenId\\",\\"createTime\\",\\"clientType\\",
        \\"clientVersion\\",\\"deviceId\\",\\"userAgent\\",\\"signInDate\\",
        year,month,day,hour,\\"weekday\\",week)
    from '{}/data/dailysignins_new.csv'
    delimiter as ',' csv header"
""".format(host, dbUser, parentDir)

print cmd

os.system(cmd)
