from pykafka import KafkaClient
import datetime
import pymongo
from pykafka.common import OffsetType
import calendar
import datetime as dt
import sys
import time
import pykafka
from pykafka.protocol import PartitionOffsetCommitRequest
import re
from datetime import date
con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.zhu_kafka
client = KafkaClient(hosts="10.28.148.136:9092,10.28.148.97:9092,10.28.148.135:9092")  #101.37.162.224  101.37.161.86  101.37.162.213          10.28.148.136,10.28.148.97,10.28.148.135

topic=client.topics['alarmsend']
#consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
now=datetime.datetime.now()
delta=datetime.timedelta(minutes=1)
delta_time=now+delta
count=0

def fetch_offsets(client, topic, offset):
    """Fetch raw offset data from a topic """
    if offset.lower() == 'earliest':
        return topic.earliest_available_offsets()
    elif offset.lower() == 'latest':
        return topic.latest_available_offsets()
    else:
        offset = dt.datetime.strptime(offset, "%Y-%m-%dT%H:%M:%S")
        offset = int(calendar.timegm(offset.utctimetuple()) * 1000)
        return topic.fetch_offset_limits(offset)

def fetch_consumer_lag(client, topic, consumer_group):
    """Get raw lag data for a topic/consumer group """
    latest_offsets = fetch_offsets(client, topic, 'latest')
    consumer = topic.get_simple_consumer(consumer_group=consumer_group,
                                         auto_start=False)
    current_offsets = consumer.fetch_offsets()
    return {p_id: (latest_offsets[p_id].offset[0], res.offset) for p_id, res in current_offsets}


#for i in consumer:
#    count+=1
while True:
    now=datetime.datetime.now()
    if now>=delta_time:
	delta_time=now+delta
        try:
	    document={"date":now}   #,"offset":i.offset,"count":count}
        except e:
	    pass
        else:
	    offset_lastest=fetch_consumer_lag(client,topic,'product')[0]
            latest_offset=offset_lastest[0]
            current_offset=offset_lastest[1]
	    lag=latest_offset-current_offset
	    document["latest_offset"]=latest_offset
	    document["current_offset"]=current_offset
	    document["lag"]=lag
            db.alarmsend.insert(document)
            #count=0


