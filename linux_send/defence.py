from pykafka import KafkaClient
from pykafka.common import OffsetType
import datetime
import pymongo
from datetime import date
con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.monitordb
client = KafkaClient(hosts="10.28.148.136:9092,10.28.148.97:9092,10.28.148.135:9092")  #101.37.162.224  101.37.161.86  101.37.162.213          10.28.148.136,10.28.148.97,10.28.148.135
topic=client.topics['alarmsend']
consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
now=datetime.datetime.now()
delta=datetime.timedelta(minutes=1)
delta_time=now+delta
count=0
http_count=0
for i in consumer:
    http_count+=1
    try:
    	now=datetime.datetime.now()
    	if now<delta_time:
	    if eval(i.value).has_key('sendMsg'):
	        data=eval(i.value)['sendMsg']
	        if int(data['alarmType'])==12:
	            count+=1
        if now>=delta_time:
	    delta_time=delta_time+delta
    	    document={"date":now,"count":count,"http_count":http_count}
    	    db.defence.insert(document)
	    count=0
	    http_count=0
        else:
	    pass
    except:
	pass



