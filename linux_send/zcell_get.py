
import re
import datetime
import pymongo
import json
con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.zhu_kafka

now=datetime.datetime.now()
delta=datetime.timedelta(minutes=1)
delta_time=now-delta

delta_1=datetime.timedelta(hours=1)
hour_ago=now-delta_1

delta_2=datetime.timedelta(days=1)
day_ago=now-delta_2

zcell=[['zcell_1','zcell_2','zcell_3'],['zcell_4','zcell_5','zcell_6'],['zcell_7','zcell_8','zcell_9'],['zcell_10','zcell_11','zcell_12'],['zcell_13','zcell_14','zcell_15']]

zcell_set={"zcell_1":[],"zcell_2":[],"zcell_3":[],"zcell_4":[],"zcell_5":[]}              #### the data will to zcell module

result=db.zcell_active.aggregate([{'$match':{'value.date':{'$gt':delta_time,'$lte':now}}}])

for item in result:
  
    del item['value']['date']
    if item['value']['zcell_id'] in zcell[0]:
        zcell_set["zcell_1"].append(item['value'])
    if item['value']['zcell_id'] in zcell[1]:
	zcell_set["zcell_2"].append(item['value'])
    if item['value']['zcell_id'] in zcell[2]:
	zcell_set["zcell_3"].append(item['value'])
    if item['value']['zcell_id'] in zcell[3]:
	zcell_set["zcell_4"].append(item['value'])
    if item['value']['zcell_id'] in zcell[4]:
	zcell_set["zcell_5"].append(item['value'])

jgcount,msgcount,send_count,alarm_count=0,0,0,0

jgpush_data=db.jgpush.aggregate([{'$match':{'date':{'$gt':hour_ago,'$lte':now}}}])   # jg push count  every minutes
for i in jgpush_data:
    jgcount+=1
zcell_set['jgcount']=jgcount

msgpush_data=db.messagepush.aggregate([{'$match':{'date':{'$gt':day_ago,'$lte':now}}}])  #  msg push count every minutes
for i in msgpush_data:
    msgcount+=1
zcell_set['msgcount']=msgcount

send_data=db.alarmsend.aggregate([{'$match':{'date':{'$gt':delta_time,'$lte':now}}}])
for i in send_data:
    #zcell_set['send_count']=i['count']
    zcell_set['send_current_offset']=i['current_offset']
    zcell_set['send_latest_offset']=i['latest_offset']
    zcell_set['send_lag']=i['lag']
alarm_data=db.alarmmessage.aggregate([{'$match':{'date':{'$gt':delta_time,'$lte':now}}}])
for i in alarm_data:
    #zcell_set['alarm_count']=i['count']
    zcell_set['alarm_current_offset']=i['current_offset']
    zcell_set['alarm_latest_offset']=i['latest_offset']
    zcell_set['alarm_lag']=i['lag']

json_data=json.dumps(zcell_set)
print json_data

 
