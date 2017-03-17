from pymongo import MongoClient
# import psycopg2
import os
import re

mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
chapters = db['chapters']

# chapters
os.system("""mongoexport -h 10.8.8.8 -d onion40-backup -c hypervideos \
    --fields name,keywords,createTime,_id \
    --type=csv -o data/hypervideos.csv""")

# replace
filename = "data/hypervideos.csv"
with open(filename, 'r') as file:
    result = re.sub(r'ObjectId\((.*?)\)', '\\1', file.read())
with open(filename, 'w') as f:
    f.write(result)

# exec dir
currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.dirname(currentDir)

# host = '10.8.2.42'
# dbUser = 'postgres'

dbUser = 'master'
host = 'onions-test0314.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'

cmd = """
    PGPASSWORD=Yangcong345 \
    psql -h {} -p 5432 \
    -U {} -d onion \
    -c "\copy video(name,keywords,\\"createTime\\",_id) \
    from '{}/data/hypervideos.csv' \
    delimiter as ',' csv header"
""".format(host, dbUser, parentDir)

os.system(cmd)
