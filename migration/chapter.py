from pymongo import MongoClient
# import psycopg2
import os
import re

mongo = MongoClient(host='10.8.8.8', port=27017, connect=True)
db = mongo['onions4']
chapters = db['chapters']

# chapters
os.system("""mongoexport -h 10.8.8.8 -d onions4 -c chapters \
    --fields subject,name,status,order,createTime,_id \
    --type=csv -o data/chapters.csv""")

# replace
filename = "data/chapters.csv"
with open(filename, 'r') as file:
    result = re.sub(r'ObjectId\((.*?)\)', '\\1', file.read())
with open(filename, 'w') as f:
    f.write(result)

currentDir = os.path.dirname(os.path.realpath(__file__))
parentDir = os.path.dirname(currentDir)
host = 'onions-test0314.cij1ctkoj9l3.rds.cn-north-1.amazonaws.com.cn'
cmd = """
    PGPASSWORD=Yangcong345 \
    psql -h {} -p 5432 \
    -U master -d mydb \
    -c "\copy chapter(subject,name,status,\\"order\\",\\"createTime\\",_id) \
    from '{}/data/chapters.csv' \
    delimiter as ',' csv header"
""".format(host, parentDir)

os.system(cmd)
