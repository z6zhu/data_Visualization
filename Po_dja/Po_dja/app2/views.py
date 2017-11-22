# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pymongo
import datetime
import re,math,os


con=pymongo.MongoClient('localhost',8081)  # test  139.196.201.208
db=con.monitordb

def hour_n(delta_h):
    all_dict={}
    x_list=[]  
    y0_list=[]                 # x data
    y1_list=[]              # very minutes count 
    y2_list=[]                # mes count
    pattern=re.compile('\d{2}:\d{2}')
    eight_bug=datetime.timedelta(hours=8)  # linux annotation---------------------------------------
    
    now=datetime.datetime.now()
    #now=now-eight_bug            # linux annotation---------------------------------------
    
    delta=datetime.timedelta(hours=delta_h)
    before_hour_n=now-delta                   # n hour before  
    
    for i in  db.msgCount.aggregate([{'$match':{'countTime':{'$gt':before_hour_n,'$lte':now}}}]):  #.sort('countTime',-1).limit(60):    #  mongodb  data
      
        if i['countTime']<=now:              #and i['countTime']>=before_hour_n
            
            xtime=i['countTime']+eight_bug     # linux annotation---------------------------------------
            s=str(xtime)
            s_val=pattern.search(s).group()
            x_list.append(s_val)
            y1_list.append(i['count']*10)
#             y0_list.append(i['count']*5)
    for i in db.httpReqCount.aggregate([{'$match':{'countTime':{'$gt':before_hour_n,'$lte':now}}}]):
        if i['countTime']<=now:
 
            y2_list.append(i['count']*10) 
    for i in db.defence.aggregate([{'$match':{'date':{'$gt':before_hour_n+eight_bug,'$lte':now+eight_bug}}}]): 
	y0_list.append(i['count']*10) 
    all_dict={"x_list":x_list,"y1_list":y1_list,"y2_list":y2_list,"y0_list":y0_list}
   
        
    json_data=json.dumps(all_dict)   
        
    return json_data
def interval(da1,da2):
    dict={}
    x_list=[]  
    y0_list=[]                 # x data
    y1_list=[]              # very minutes count 
    y2_list=[]                # mes count
    pattern=re.compile('\d{2}:\d{2}')
    eight_bug=datetime.timedelta(hours=8)  # linux annotation---------------------------------------
    
    redata1=re.match("(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})",da1)
    redata2=re.match("(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2})",da2)

    #del_time=datetime.timedelta(hours=8)            # must do it

    data1_year,data1_month,data1_day,data1_hour,data1_minute=int(redata1.group(1)),int(redata1.group(2)),int(redata1.group(3)),int(redata1.group(4)),int(redata1.group(5))
    data2_year,data2_month,data2_day,data2_hour,data2_minute=int(redata2.group(1)),int(redata2.group(2)),int(redata2.group(3)),int(redata2.group(4)),int(redata2.group(5))


    all_data1=datetime.datetime(year=data1_year, month=data1_month, day=data1_day, hour=data1_hour, minute=data1_minute, second=0, microsecond=0, tzinfo=None)
    #all_data1=all_data1-eight_bug
    all_data2=datetime.datetime(year=data2_year, month=data2_month, day=data2_day, hour=data2_hour, minute=data2_minute, second=0, microsecond=0, tzinfo=None)
    #all_data2=all_data2-eight_bug
    
    for i in  db.msgCount.aggregate([{'$match':{'countTime':{'$gt':all_data1-eight_bug,'$lte':all_data2-eight_bug}}}]):  #.sort('countTime',-1).limit(60):    #  mongodb  data
      
        if i['countTime']<=all_data2:              #and i['countTime']>=before_hour_n
            
            xtime=i['countTime']+eight_bug     # linux annotation---------------------------------------
            s=str(xtime)
            s_val=pattern.search(s).group()
            x_list.append(s_val)
            y1_list.append(i['count']*10)
#             y0_list.append(i['count']*5)
    for i in db.httpReqCount.aggregate([{'$match':{'countTime':{'$gt':all_data1-eight_bug,'$lte':all_data2-eight_bug}}}]):
        if i['countTime']<=all_data2:
 
            y2_list.append(i['count']*10)
    for i in db.defence.aggregate([{'$match':{'date':{'$gt':all_data1-eight_bug,'$lte':all_data2-eight_bug}}}]):
        if i['date']<=all_data2:
            y0_list.append(i['count']*10)
                
    dict={"x_list":x_list,"y1_list":y1_list,"y2_list":y2_list,"y0_list":y0_list}
    json_go=json.dumps(dict)   
        
    return json_go
        
@csrf_exempt
def map_char1(request):
    #return HttpResponse("test")
    if request.is_ajax() and request.method == 'GET':
        print request.GET
        if request.GET.get('value'):
            if request.GET.get('value')=="1":
                ret_val=hour_n(1)
                return HttpResponse(ret_val)
            elif request.GET.get('value')=="2":
                ret_val=hour_n(3)
                return HttpResponse(ret_val)
            elif request.GET.get('value')=="3":
                ret_val=hour_n(6)
                return HttpResponse(ret_val)
            elif request.GET.get('value')=="4":
                ret_val=hour_n(12)
                return HttpResponse(ret_val)
            elif request.GET.get('value')=="5":
                ret_val=hour_n(24)
                return HttpResponse(ret_val)
            else:
                print "-------------------------------error----------------------------"
    if request.is_ajax() and request.method == 'POST':
        
        if request.POST.get('data_date1') and request.POST.get('data_date2'):
            
            da1=request.POST.get('data_date1') 
            da2=request.POST.get('data_date2') 
            jdata=interval(da1,da2) 
            return HttpResponse(jdata)
                          
    return render(request,"char_map_line.html")

def do_te(request):
    #return HttpResponse("test")
    return render(request,"test.html")
