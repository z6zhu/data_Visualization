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

for i in db.alarmmessage_zone.find().sort("date",-1).limit(1):
    print i
    del i['date']
    del i['_id']
    shop_month=sorted(i.iteritems(),key=lambda dic:dic[1],reverse=True)
    print shop_month
