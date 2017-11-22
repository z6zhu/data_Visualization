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

pattern=re.compile(ur'有限[\u4e00-\u9fa5]*' )
mysql_dict={}
temp_dict={}

cursor.execute("""select companyId,companyName from y_info_company""")
data=cursor.fetchall()
for i in data:
    t=re.sub(pattern,"", i[1])
    mysql_dict[str(i[0])]=t
#print mysql_dict


client = KafkaClient(hosts="10.28.148.136:9092,10.28.148.97:9092,10.28.148.135:9092")  #101.37.162.224  101.37.161.86  101.37.162.213          10.28.148.136,10.28.148.97,10.28.148.135
topic=client.topics['alarmsend']
consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
now=datetime.datetime.now()
delta=datetime.timedelta(minutes=5)
delta_time=now+delta
document={}
for i in consumer:
    try:
    	now=datetime.datetime.now()
    	if now<delta_time:
	    if eval(i.value).has_key('sendMsg'):
	        data=eval(i.value)['sendMsg']
	        if int(data['alarmType'])==12:
		   # print eval(i.value)['companyId']
		    if document.has_key(eval(i.value)['companyId']):
   	                document[eval(i.value)['companyId']]+=1
		    else:
			document[eval(i.value)['companyId']]=1
        if now>=delta_time:
	    delta_time=delta_time+delta
            
            for i in document:
		if mysql_dict.has_key(i):
		    temp_dict[mysql_dict[i]]=document[i]
            temp_dict['date']=now
    	    db.defence_zone.insert(temp_dict)
	    document={}
	    temp_dict={}
        else:
	    pass
    except:
	pass



