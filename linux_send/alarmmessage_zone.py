# -*- coding: utf-8 -*-
from pykafka import KafkaClient
from pykafka.common import OffsetType
import datetime
import pymongo
import MySQLdb
import re
from datetime import date
con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.zhu_kafka

sqldb = MySQLdb.connect(host='rds7m888213p5s6g4xgo.mysql.rds.aliyuncs.com', port=3306, user='huangwenbo', passwd='hwb_123_JX', db='jx_security', charset="UTF8")
cursor = sqldb.cursor()

pattern=re.compile(r'(\d{2})(\d{3})(\d{2})')
patt=re.compile(ur'有限[\u4e00-\u9fa5]*' )
mysql_dict={}
temp_dict={}

cursor.execute("""select companyId,companyName from y_info_company""")
data=cursor.fetchall()
for i in data:
    t=re.sub(patt,"", i[1])
    mysql_dict[str(i[0])]=t
#print mysql_dict


client = KafkaClient(hosts="10.28.148.136:9092,10.28.148.97:9092,10.28.148.135:9092")  #101.37.162.224  101.37.161.86  101.37.162.213          10.28.148.136,10.28.148.97,10.28.148.135
topic=client.topics['alarmmessage']
consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
now=datetime.datetime.now()
delta=datetime.timedelta(minutes=1)
delta_time=now+delta
document={}
tmp_dict={}
for i in consumer:
    try:
    	now=datetime.datetime.now()
    	if now<delta_time:
	    node= eval(i.value)['params']['data'][0]['node']

	    number=str(int(pattern.search(node).group(2)))

	    if document.has_key(number):
                document[number]+=1
            else:
	        document[number]=1
           
        if now>=delta_time:
	    delta_time=delta_time+delta
        #   print document
            for i in document:
		if mysql_dict.has_key(i):
		    temp_dict[mysql_dict[i]]=document[i]

            temp_dict['date']=now
 
	#    print temp_dict
            db.alarmmessage_zone.insert(temp_dict)
	    document={}
	    temp_dict={}
    except:
	pass




