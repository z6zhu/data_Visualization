

from pykafka import KafkaClient
import re
import datetime
import pymongo
from pykafka.common import OffsetType
client = KafkaClient(hosts="10.28.148.136:9092,10.28.148.97:9092,10.28.148.135:9092")  #101.37.162.224  101.37.161.86  101.37.162.213          10.28.148.136,10.28.148.97,10.28.148.135

con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.zhu_kafka


topic=client.topics['Hostmodule_run_number']



consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
#consumer=topic.get_simple_consumer()
for i in consumer:
    #print i.value,i.offset
    document={"offset":i.offset,"value":eval(i.value)}
    db.zcell_active.insert(document)

