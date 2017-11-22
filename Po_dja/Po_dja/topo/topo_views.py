# _*_ coding: utf-8 _*_
from __future__ import unicode_literals
from django.shortcuts import render
import json
import datetime
from django.http.request import HttpRequest
from django.http.response import HttpResponse  
import pymongo
import MySQLdb
import re
from django.views.decorators.csrf import csrf_exempt
con=pymongo.MongoClient('127.0.0.1',27017)   #'121.40.216.11',8081
db=con.zhu_kafka
req=con.monitordb
#local   rds7m888213p5s6g4xgoo.mysql.rds.aliyuncs.com
#sqldb= MySQLdb.connect("rds7m888213p5s6g4xgoo.mysql.rds.aliyuncs.com","huangwenbo","hwb_123_JX","jx_security", charset="UTF8") 
#online use // inner 
sqldb=MySQLdb.connect(host='rds7m888213p5s6g4xgo.mysql.rds.aliyuncs.com', port=3306, user='huangwenbo', passwd='hwb_123_JX', db='jx_security', charset="UTF8")
cursor = sqldb.cursor()
#import re,math,os  #106.14.173.0
# Create your views here.
pattern=re.compile(ur'有限[\u4e00-\u9fa5]*' )
def shop_sql():
    cursor.execute("""
    SELECT COUNT(1) FROM `s_shop` WHERE isUsing = 1 AND shopState = 1 AND isDelete=0
    """)
    data = cursor.fetchone()
    return data[0]
def user_sql():
    cursor.execute("""
    SELECT COUNT(1) FROM y_info_account WHERE isDelete = 0
    """)
    data = cursor.fetchone()
    return data[0]
def shop_every_month():
    shop_month={}
    cursor.execute("""
    SELECT a.companyId, ( SELECT companyName FROM y_info_company b WHERE a.companyId = b.companyId ) AS companyName, a.num 
    FROM (SELECT companyId, COUNT(1) AS num FROM `s_shop` 
    WHERE isUsing = 1 AND shopState = 1 AND isDelete=0 AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(createDate)
    GROUP BY companyId ) a
    order by a.num desc
    limit 10
    """)
    
    data = cursor.fetchall()
#     print '-------------------------',data
    for i in data:
        if i[0]==0:
	    pass
        else:
#       tt=str(i[1]).decode('utf-8')
            t=re.sub(pattern,"", i[1])
            shop_month[t]=i[2]
            print t,shop_month[t]
    return sorted(shop_month.iteritems(),key=lambda dic:dic[1],reverse=True)   
def user_every_month():
    user_month={}
    user_dict1={}
    user_dict2={}
    user_dict3={}
    user_dict4={}
    """=============e dun =================="""
    cursor.execute("""
    SELECT tt.companyId, ( SELECT cc.companyName FROM y_info_company cc WHERE cc.isUsing=1 AND cc.isDelete=0 AND  cc.companyId = 
    tt.companyId ) AS companyName, tt.num FROM (SELECT t.companyId, COUNT(1) AS num FROM y_info_account a, (SELECT c.companyId, b.accountId FROM s_shop c, 
    c_account_shop b WHERE c.shopId = b.shopId AND c.isDelete = 0 AND c.shopState = 1 AND c.isUsing = 1 AND b.isDelete = 0 AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(c.createDate)) t 
    WHERE t.accountId = a.accountId AND a.isDelete = 0 
    GROUP BY t.companyId ) tt
    ORDER BY num desc
    """)
    data1=cursor.fetchall()
    
#     print '-------------------------',data1
     
    for i in data1:
        if i[0]==0:
            pass
        else:

            t=re.sub(pattern,"", i[1])
#           print i[1],i[2]
            user_dict1[t]=i[2]
    
      
    """============= zong guan=================="""
    cursor.execute("""
    SELECT t.companyId, ( SELECT e.companyName FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
    companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
    r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 2 AND a.isDelete = 0 AND b.isDelete = 0 AND 
    DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(b.createDate) ) d 
    WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
    """)
    data2=cursor.fetchall()
    for i in data2:
	if i[0]==0:
            pass
        else:

            t=re.sub(pattern,"", i[1])
#           print i[1],i[2]
            user_dict2[t]=i[2]
     
    """==============hu wei ========================"""
    cursor.execute("""
    SELECT t.companyId, ( SELECT e.companyName FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
    companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
    r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 5 AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(b.createDate) AND a.isDelete = 0 
    AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
    """)
    data3=cursor.fetchall()
    for i in data3:
	if i[0]==0:
            pass
        else:

#         print i[1],i[2]
            t=re.sub(pattern,"", i[1])
            user_dict3[t]=i[2]
     
    """==============zhong xin ========================"""
    cursor.execute("""
    SELECT t.companyId, ( SELECT e.companyName FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
    companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
    r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 3 AND DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(b.createDate) AND a.isDelete = 0 
    AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
    """)
    data4=cursor.fetchall()
    for i in data4:
	if i[0]==0:
            pass
        else:

#         print i[1],i[2]
            t=re.sub(pattern,"", i[1])
            user_dict4[t]=i[2]
         
    user_month=cobina(cobina(cobina(user_dict1,user_dict2),user_dict3),user_dict4)

    return sorted(user_month.iteritems(),key=lambda dic:dic[1],reverse=True)[0:10]
#     for i in lisss:
#         print i[0],i[1]
def cobina(dict,dict1):  # this function is to add 3app+1client number 
    lis=dict.keys()
    lis1=dict1.keys()
    for i in lis1:
        if dict.has_key(i):
            dict[i]=dict[i]+dict1[i]
            
        else:
            dict[i]=dict1[i]
    return dict

result={}  # resutl is for zcell data 
@csrf_exempt
def topo(request):
    if request.is_ajax() and request.method == 'GET' and request.GET.get('data')=='1':
        now=datetime.datetime.now()
        delta_1=datetime.timedelta(hours=8)
        after_now=now+delta_1
        delta=datetime.timedelta(days=1)
	day_ago=now-delta
	msgcount=0
        
        print "---------------start----------------------------"
        count=0
        zcell2=db.zcell_active.find({"value.zcell_id":"zcell_2"}).sort("offset",-1).limit(2)
        for i in zcell2: 
            if count>0: 
                result['zcell_2']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_2']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:   
                result.update({"zcell_2":{"zcell_id":"zcell_2","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
                count+=1
        zcell3=db.zcell_active.find({"value.zcell_id":"zcell_3"}).sort("offset",-1).limit(2)
        for i in zcell3:
            if count>0: 
                result['zcell_3']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_3']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:   
                result.update({"zcell_3":{"zcell_id":"zcell_3","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell4=db.zcell_active.find({"value.zcell_id":"zcell_4"}).sort("offset",-1).limit(2)
    	for i in zcell4:
            if count>0: 
                result['zcell_4']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_4']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_4":{"zcell_id":"zcell_4","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell5=db.zcell_active.find({"value.zcell_id":"zcell_5"}).sort("offset",-1).limit(2)
    	for i in zcell5:
            if count>0: 
                result['zcell_5']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_5']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_5":{"zcell_id":"zcell_5","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell6=db.zcell_active.find({"value.zcell_id":"zcell_6"}).sort("offset",-1).limit(2)
    	for i in zcell6:
            if count>0: 
                result['zcell_6']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_6']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_6":{"zcell_id":"zcell_6","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell7=db.zcell_active.find({"value.zcell_id":"zcell_7"}).sort("offset",-1).limit(2)
    	for i in zcell7:
            if count>0: 
                result['zcell_7']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_7']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_7":{"zcell_id":"zcell_7","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell8=db.zcell_active.find({"value.zcell_id":"zcell_8"}).sort("offset",-1).limit(2)
    	for i in zcell8:
            if count>0: 
                result['zcell_8']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_8']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_8":{"zcell_id":"zcell_8","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell10=db.zcell_active.find({"value.zcell_id":"zcell_10"}).sort("offset",-1).limit(2)
    	for i in zcell10:
            if count>0: 
                result['zcell_10']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_10']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_10":{"zcell_id":"zcell_10","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell11=db.zcell_active.find({"value.zcell_id":"zcell_11"}).sort("offset",-1).limit(2)
    	for i in zcell11:
            if count>0: 
                result['zcell_11']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_11']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_11":{"zcell_id":"zcell_11","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell12=db.zcell_active.find({"value.zcell_id":"zcell_12"}).sort("offset",-1).limit(2)
    	for i in zcell12:
            if count>0: 
                result['zcell_12']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_12']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_12":{"zcell_id":"zcell_12","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell13=db.zcell_active.find({"value.zcell_id":"zcell_13"}).sort("offset",-1).limit(2)
    	for i in zcell13:
            if count>0: 
                result['zcell_13']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_13']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_13":{"zcell_id":"zcell_13","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell14=db.zcell_active.find({"value.zcell_id":"zcell_14"}).sort("offset",-1).limit(2)
    	for i in zcell14:
            if count>0: 
                result['zcell_14']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_14']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_14":{"zcell_id":"zcell_14","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
    	        count+=1
        zcell15=db.zcell_active.find({"value.zcell_id":"zcell_15"}).sort("offset",-1).limit(2)
    	for i in zcell15:
            if count>0: 
                result['zcell_15']['current_offset_sum'].append(sum(i['value']['current_offset']))
                result['zcell_15']['latest_offset_sum'].append(sum(i['value']['latest_offset']))
                count-=1
            else:
                result.update({"zcell_15":{"zcell_id":"zcell_15","host_number":i['value']['host_number'],"lag_sum":sum(i['value']['lag']),"current_offset_sum":[sum(i['value']['current_offset'])],"latest_offset_sum":[sum(i['value']['latest_offset'])]}})
                count+=1
          
        for i in req.httpReqCount.find().sort('countTime',-1).limit(1):  #aggregate([{'$match':{'countTime':{'$gt':mongo_ago,'$lte':now}}}])  #  web count every minutes
            result['web_request']=i['count']
            
#        for i in db.jgpush.aggregate([{'$match':{'date':{'$gt':minutes_ago,'$lte':now}}}]):   # jg push count  every minutes
#            jgcount+=1
#        result['jgcount']=jgcount

        for i in db.messagepush.aggregate([{'$match':{'date':{'$gt':day_ago,'$lte':after_now}}}]):  #  msg push count every minutes
            msgcount+=1
        print '---------------------',msgcount
        result['msgcount']=msgcount
        
        pattern=re.compile('\d{2}:\d{2}')    
        
	result['jgpush_current_offset']=[]
        result['jgpush_latest_offset']=[]

        for i in db.jgpush.find().sort("date",-1).limit(2):
            result['jgpush_current_offset'].insert(0,i['current_offset'])
            result['jgpush_latest_offset'].insert(0,i['latest_offset'])

	result['alarm_current_offset']=[]
        result['alarm_latest_offset']=[]
#         result['alarm_date']=[]
#         result['alarm_lag']=[]
        
        for i in db.alarmmessage.find().sort("date",-1).limit(2):
            result['alarm_current_offset'].insert(0,i['current_offset'])
            result['alarm_latest_offset'].insert(0,i['latest_offset'])
#             result['alarm_date'].insert(0,pattern.search(str(i['date'])).group())
#             result['alarm_lag'].insert(0,i['lag'])
#         result['alarm_lag']=result['alarm_lag'][-1:][0]

        result['send_current_offset']=[]
        result['send_latest_offset']=[] 
        result['send_date']=[] 
        result['send_lag']=[]
        
        for i in db.alarmsend.find().sort("date",-1).limit(2):   #aggregate([{'$match':{'date':{'$gt':delta_time,'$lte':now}}}])
            result['send_current_offset'].insert(0,i['current_offset'])
            result['send_latest_offset'].insert(0,i['latest_offset'])
#             result['send_date'].insert(0,pattern.search(str(i['date'])).group())
#             result['send_lag'].insert(0,i['lag'])               
#         result['send_lag']=result['send_lag'][-1:][0]
#         print result
        json_data=json.dumps(result)
        return HttpResponse(json_data) 
    if request.is_ajax() and request.method == 'GET' and request.GET.get('data')=='2':
        



	now=datetime.datetime.now()
        delta=datetime.timedelta(days=1)
        deltime=now-delta
       
        
        pg=req.defence.aggregate( [{'$match':{'date':{'$gt':deltime,'$lte':now} } },{'$group':{'_id':"null",'num_tutorial':{'$sum':"$count"}}}] )
	for i in pg:
    	   shop= i['num_tutorial']

	print shop

	ng=db.alarmmessage.aggregate( [{'$match':{'date':{'$gt':deltime,'$lte':now} } },{'$group':{'_id':"null",'num_tutorial':{'$max':"$current_offset"}}}] )
	for i in ng:
    	    max_num=i['num_tutorial']


	gg=db.alarmmessage.aggregate( [{'$match':{'date':{'$gt':deltime,'$lte':now} } },{'$group':{'_id':"null",'num_tutorial':{'$min':"$current_offset"}}}] )
	for i in gg:
            min_num=i['num_tutorial']

	user= max_num-min_num 
        print '-----------',user


 #	shop=shop_sql()
 #       user=user_sql()

	for i in db.alarmmessage_zone.find().sort("date",-1).limit(1):
            del i['date']
            del i['_id']
            shop_month=sorted(i.iteritems(),key=lambda dic:dic[1],reverse=True)
        
#        shop_month=shop_every_month()

#         for i in shop_month:
#             print i[0],i[1]
	for i in db.defence_zone.find().sort("date",-1).limit(1):
            del i['date']
            del i['_id']
            user_month=sorted(i.iteritems(),key=lambda dic:dic[1],reverse=True)
#        user_month=user_every_month()
#         for i in user_month:
#             print i[0],i[1]
        
        dict={'shop':shop,'user':user,'shop_month':shop_month,'user_month':user_month}

        json_go=json.dumps(dict)
        return HttpResponse(json_go)
    if request.is_ajax() and request.method == 'GET' and request.GET.get('data')=='3':
        zcell_detail=db.zcell_active.find({"value.zcell_id":request.GET.get('zcell_num')}).sort("offset",-1).limit(1)
        
        print '------------------------------',zcell_detail
        for i in zcell_detail: 
            print i  
            module=i['value']['module_active']
        dict3={'module':module}
        json_qu=json.dumps(dict3)
        return HttpResponse(json_qu)
    return render(request,'detail.html')


