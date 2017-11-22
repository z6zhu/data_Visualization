# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
import random
from django.http.response import HttpResponse  
import os
import re
import MySQLdb
import datetime
import json 
db = MySQLdb.connect("rds7m888213p5s6g4xgo.mysql.rds.aliyuncs.com","huangwenbo","hwb_123_JX","jx_security", charset="UTF8") 
cursor = db.cursor()
patt = re.compile(ur'[\u4E00-\u9FA5]{2}')
pattern=re.compile(ur'有限[\u4e00-\u9fa5]*' )
def show_data(data):
    dict={}
    add_list=[]
    data_list=[]
    for i in data:
        if i[1]==None:
            pass
        else:
            addr=patt.search(i[1]).group()
            if not dict.has_key(addr):
                dict[addr]=i[2]
            else:
                dict[addr]=dict[addr]+i[2]
    the_sum=sum(dict.values())
    #dict=sorted(dict.iteritems(),key=lambda d:d[1],reverse=True)
    dict=dict.items()
    for i in dict:
        add_list.append(i[0])
        data_list.append(i[1])
    return the_sum,add_list,data_list
def e_dun():
    cursor.execute("""
SELECT tt.companyId, ( SELECT cc.companyAddress FROM y_info_company cc WHERE cc.isUsing=1 AND cc.isDelete=0 AND  cc.companyId = 
tt.companyId ) AS companyName, tt.num FROM (SELECT t.companyId, COUNT(1) AS num FROM y_info_account a, (SELECT c.companyId, b.accountId FROM s_shop c, 
c_account_shop b WHERE c.shopId = b.shopId AND c.isDelete = 0 AND c.shopState = 1 AND c.isUsing = 1 AND b.isDelete = 0 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now()) t 
WHERE t.accountId = a.accountId AND a.isDelete = 0 
GROUP BY t.companyId ) tt
""")
    data1=cursor.fetchall()
    dun_sum,dun_add_list,dun_data_list=show_data(data1)
    return dun_sum,dun_add_list,dun_data_list
def e_dun_active():
    cursor.execute("""
SELECT tt.companyId, ( SELECT cc.companyAddress FROM y_info_company cc WHERE cc.isUsing=1 AND cc.isDelete=0 AND  cc.companyId = 
tt.companyId ) AS companyName, tt.num FROM (SELECT t.companyId, COUNT(1) AS num FROM y_info_account a, (SELECT c.companyId, b.accountId FROM s_shop c, 
c_account_shop b WHERE c.shopId = b.shopId AND c.isDelete = 0 AND c.shopState = 1 AND c.isUsing = 1 AND b.isDelete = 0 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now()) t 
WHERE t.accountId = a.accountId AND a.isDelete = 0 AND activated=1
GROUP BY t.companyId ) tt
""")
    data1=cursor.fetchall()
    dun_sum,dun_add_list,dun_data_list=show_data(data1)
    return dun_sum,dun_add_list,dun_data_list

def e_dun_online():
    cursor.execute("""
SELECT tt.companyId, ( SELECT cc.companyAddress FROM y_info_company cc WHERE cc.isUsing=1 AND cc.isDelete=0 AND  cc.companyId = 
tt.companyId ) AS companyName, tt.num FROM (SELECT t.companyId, COUNT(1) AS num FROM (select * from y_info_account where DATE_SUB(curdate(), INTERVAL 30 DAY) <= date(modifyDate)) a, (SELECT c.companyId, b.accountId FROM s_shop c, 
c_account_shop b WHERE c.shopId = b.shopId AND c.isDelete = 0 AND c.shopState = 1 AND c.isUsing = 1 AND b.isDelete = 0 AND b.createDate <= now()) t 
WHERE t.accountId = a.accountId AND a.isDelete = 0 
GROUP BY t.companyId ) tt
""")
    data1_online=cursor.fetchall()
    dun_sum_online,dun_add_list_online,dun_data_list_online=show_data(data1_online)
    return dun_sum_online,dun_add_list_online,dun_data_list_online

def e_dun_islogin():
    cursor.execute("""
SELECT tt.companyId, ( SELECT cc.companyAddress FROM y_info_company cc WHERE cc.isUsing=1 AND cc.isDelete=0 AND  cc.companyId = 
tt.companyId ) AS companyName, tt.num FROM (SELECT t.companyId, COUNT(1) AS num FROM (select * from y_info_account where DATE_SUB(curdate(), INTERVAL 30 DAY) <= date(modifyDate)) a, (SELECT c.companyId, b.accountId FROM s_shop c, 
c_account_shop b WHERE c.shopId = b.shopId AND c.isDelete = 0 AND c.shopState = 1 AND c.isUsing = 1 AND b.isDelete = 0 AND b.createDate <= now()) t 
WHERE t.accountId = a.accountId AND a.isDelete = 0 AND a.isLogin=1
GROUP BY t.companyId ) tt
""")
    data1_online=cursor.fetchall()
    dun_sum_online,dun_add_list_online,dun_data_list_online=show_data(data1_online)
    return dun_sum_online,dun_add_list_online,dun_data_list_online


def zong_guan():
    cursor.execute("""
    SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
    companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
    r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 2 AND a.isDelete = 0 AND b.isDelete = 0 AND 
    DATE_FORMAT(b.createDate, '%Y%m%d') <= now() ) d 
    WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
    """)
    data2=cursor.fetchall()
    guan_sum,guan_add_list,guan_data_list=show_data(data2)
    return guan_sum,guan_add_list,guan_data_list

def zong_guan_online():
    cursor.execute("""
    SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
    companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM (select * from c_info_employee where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(modifyDate)) c, (SELECT a.employeeId FROM c_info_employee_role a, 
    r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 2 AND a.isDelete = 0 AND b.isDelete = 0 AND 
    DATE_FORMAT(b.createDate, '%Y%m%d') <= now() ) d 
    WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
    """)
    data2=cursor.fetchall()
    guan_sum_online,guan_add_list_online,guan_data_list_online=show_data(data2)
    return guan_sum_online,guan_add_list_online,guan_data_list_online

def  hu_wei():  
    cursor.execute("""
SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 5 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now() AND a.isDelete = 0 
AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
""")
    data3=cursor.fetchall()
    hu_sum,hu_add_list,hu_data_list=show_data(data3)
#     print hu_sum
#     for i in range(len(hu_add_list)):
#         print hu_add_list[i],hu_data_list[i]
    return hu_sum,hu_add_list,hu_data_list
      
def  hu_wei_online():    
    cursor.execute("""
SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM (select * from c_info_employee where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(modifyDate)) c, (SELECT a.employeeId FROM c_info_employee_role a, 
r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 5 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now() AND a.isDelete = 0 
AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
""")
    data3=cursor.fetchall()
    hu_sum_online,hu_add_list_online,hu_data_list_online=show_data(data3)
#     print hu_sum
#     for i in range(len(hu_add_list)):
#         print hu_add_list[i],hu_data_list[i]
    return  hu_sum_online,hu_add_list_online,hu_data_list_online

def zhong_xin():
    cursor.execute("""
SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM c_info_employee c, (SELECT a.employeeId FROM c_info_employee_role a, 
r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 3 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now() AND a.isDelete = 0 
AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
""")
    data4=cursor.fetchall()
    xin_sum,xin_add_list,xin_data_list=show_data(data4)
#     print xin_sum
#     for i in range(len(xin_add_list)):
#         print xin_add_list[i],xin_data_list[i]
    return xin_sum,xin_add_list,xin_data_list

def zhong_xin_online():
    cursor.execute("""
SELECT t.companyId, ( SELECT e.companyAddress FROM y_info_company e WHERE e.isUsing=1 AND e.isDelete=0 AND e.companyId = t.companyId ) AS 
companyName, t.num FROM (SELECT c.companyId, COUNT(1) AS num FROM (select * from c_info_employee where DATE_SUB(CURDATE(), INTERVAL 30 DAY) <= date(modifyDate)) c, (SELECT a.employeeId FROM c_info_employee_role a, 
r_roler_function b WHERE a.roleId = b.rolerId AND b.functionId = 3 AND DATE_FORMAT(b.createDate, '%Y%m%d') <= now() AND a.isDelete = 0 
AND b.isDelete = 0 ) d WHERE c.employeeId = d.employeeId AND c.isDelete = 0 GROUP BY c.companyId ) t
""")
    data4=cursor.fetchall()
    xin_sum_online,xin_add_list_online,xin_data_list_online=show_data(data4)
#     print xin_sum
#     for i in range(len(xin_add_list)):
#         print xin_add_list[i],xin_data_list[i]
    return xin_sum_online,xin_add_list_online,xin_data_list_online


def append_list(add_list,add_list_online,data_list_online):
    list=[]
    for i in add_list:
        if i in add_list_online:
            list.append(data_list_online[add_list_online.index(i)])
        else:
            list.append(0)
    return list
#------------------------------------------------------------------------------------------------------------------------------------------
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
    for i in data1:
        if i[0]==0:
            pass
        else:
            t=re.sub(pattern,"", i[1])
#         print i[1],i[2]
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
#         print i[1],i[2]
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
    return sorted(user_month.iteritems(),key=lambda dic:dic[1],reverse=True)

def online_shop():
    cursor.execute("""
SELECT d.companyId, e.companyAddress, SUM(CASE WHEN onLineState = 0 AND (deviceStyle = 3 OR deviceStyle = 4) THEN 1 ELSE 0 END) AS onLineCount FROM s_shop_device c LEFT JOIN s_shop d ON c.shopId = d.shopId LEFT JOIN 
y_info_company e ON e.companyId = d.companyId WHERE c.isDelete = 0 AND DATE_FORMAT(c.createDate, '%Y%m%d') <=NOW()  GROUP BY d.companyId
""")
    data=cursor.fetchall()
    the_sum,add_list,data_list=show_data(data)
    return the_sum,add_list,data_list
    
def offline_shop():
    cursor.execute("""
SELECT d.companyId, e.companyAddress, SUM(CASE WHEN onLineState = 1 AND (deviceStyle = 3 OR deviceStyle = 4) THEN 1 ELSE 0 END) AS onLineCount FROM s_shop_device c LEFT JOIN s_shop d ON c.shopId = d.shopId LEFT JOIN 
y_info_company e ON e.companyId = d.companyId WHERE c.isDelete = 0 AND DATE_FORMAT(c.createDate, '%Y%m%d') <=NOW()  GROUP BY d.companyId
""")
    data=cursor.fetchall()
    the_sum,add_list,data_list=show_data(data)
    return the_sum,add_list,data_list

def cobina(dict,dict1):  # this function is to add 3app+1client number 
    lis=dict.keys()
    lis1=dict1.keys()
    for i in lis1:
        if dict.has_key(i):
            dict[i]=dict[i]+dict1[i]
            
        else:
            dict[i]=dict1[i]
    return dict
def change_list(list):
    tt=[]
    for i in list:
        if i>0 and i<=100:
            tt.append(i*100+13)
        if i>100 and i<=300:
            tt.append(i*30)
        if i>300 and i<=1000:
            tt.append(i*10)
        if i>1000 and i<=5000:
            tt.append(i*5)
        if i>5000:
            tt.append(i)
    return tt
def user_shop(request):
    
    json_dict={}
    
    if request.is_ajax() and request.method == 'GET':
        #=================================================================start=====================================================
        print '================shop account================='
        cursor.execute("""
    SELECT COUNT(1) FROM `s_shop` WHERE isUsing = 1 AND shopState = 1 AND isDelete=0
    """)
        data = cursor.fetchone()
        json_dict['shop']=data[0]
        print '==============user account==================='
        cursor.execute("""
    SELECT COUNT(1) FROM y_info_account WHERE isDelete = 0
    """)
        data = cursor.fetchone()
        json_dict['user']=data[0]
    
        """=============e dun active and online========================================================="""  
        dun_sum,dun_add_list,dun_data_list=e_dun()
        dun_sum_active,dun_add_list_active,dun_data_list_active=e_dun_active()
        dun_sum_online,dun_add_list_online,dun_data_list_online=e_dun_online()
        dun_sum_login,dun_add_list_login,dun_data_list_login=e_dun_islogin()
        
        dun_active=append_list(dun_add_list, dun_add_list_active, dun_data_list_active) 
        dun_construct=append_list(dun_add_list, dun_add_list_online, dun_data_list_online) 
        dun_login=append_list(dun_add_list, dun_add_list_login, dun_data_list_login) 
             
        
        json_dict['dun_add_list']=dun_add_list
        
        dun_data_list=change_list(dun_data_list)
        json_dict['dun_data_list']=dun_data_list
        
        
        dun_active=change_list(dun_active)
        json_dict['dun_active']=dun_active
        
        dun_construct=change_list(dun_construct)
        json_dict['dun_construct']=dun_construct
        json_dict['dun_login']=dun_login
        

   #     print dun_sum,dun_sum_online
   #     for i in range(len(dun_add_list)):
   #         print dun_add_list[i],dun_data_list[i],dun_active[i],dun_construct[i],dun_login[i]
      
        """============= zong guan and online======================================================"""    
        guan_sum,guan_add_list,guan_data_list=zong_guan()
        guan_sum_online,guan_add_list_online,guan_data_list_online=zong_guan_online()
        guan_construct=append_list(guan_add_list,guan_add_list_online, guan_data_list_online) 
        
        
        json_dict['guan_sum']=guan_sum
        json_dict['guan_sum_online']=guan_sum_online
        
        json_dict['guan_add_list']=guan_add_list
        json_dict['guan_data_list']=guan_data_list
        json_dict['guan_construct']=guan_construct

   #     print guan_sum,guan_sum_online
   #     for i in range(len(guan_add_list)):
   #         print guan_add_list[i],guan_data_list[i],guan_construct[i]
    
        """==============hu wei and online========================"""
        hu_sum,hu_add_list,hu_data_list=hu_wei()
        hu_sum_online,hu_add_list_online,hu_data_list_online=hu_wei_online()
        hu_construct=append_list(hu_add_list, hu_add_list_online, hu_data_list_online) 
        
        json_dict['hu_sum']=hu_sum
        json_dict['hu_sum_online']=hu_sum_online
        
        json_dict['hu_add_list']=hu_add_list
        json_dict['hu_data_list']=hu_data_list
        json_dict['hu_construct']=hu_construct

   #     print hu_sum,hu_sum_online
   #     for i in range(len(hu_add_list)):
   #         print hu_add_list[i],hu_data_list[i],hu_construct[i]
 
        """=============zhong xin and online ========================"""
        xin_sum,xin_add_list,xin_data_list=zhong_xin()
        xin_sum_online,xin_add_list_online,xin_data_list_online=zhong_xin_online()
        xin_construct=append_list(xin_add_list, xin_add_list_online, xin_data_list_online) 
        
        json_dict['xin_sum']=xin_sum
        json_dict['xin_sum_online']=xin_sum_online
        
        json_dict['xin_add_list']=xin_add_list
        json_dict['xin_data_list']=xin_data_list
        json_dict['xin_construct']=xin_construct
        

  #      print xin_sum,xin_sum_online
   #     for i in range(len(xin_add_list)):
   #         print xin_add_list[i],xin_data_list[i],xin_construct[i]
        """=======================start======================="""
        shop_month=shop_every_month()
        
        json_dict['shop_month']=shop_month
        
  #      for i in shop_month:
  #          print i[0],i[1]
        user_month=user_every_month()
        
    #    print '=====================================================',shop_month
        
        json_dict['user_month']=user_month
        
        
        
   #     for i in user_month:
    #        print i[0],i[1]
        
        """----------------------------online----------------------------"""
        the_sum,add_list_online,data_list_online=online_shop()
    #    for i in range(len(add_list_online)):
   #         print add_list_online[i],data_list_online[i]
        """----------------------------offline----------------------------"""
        the_sum,add_list_offline,data_list_offline=offline_shop()
    #    for i in range(len(add_list_offline)):
     #       print add_list_offline[i],data_list_offline[i]
    
        resort=append_list(add_list_online, add_list_offline, data_list_offline)
    #    for i in range(len(add_list_online)):
    #        print add_list_online[i],data_list_online[i],resort[i]
             
        json_dict['add_list_online']=add_list_online
        zone_online=[]
        zone_offline=[]
        for i in data_list_online:
            zone_online.append(int(i))
        json_dict['data_list_online']=zone_online
        for i in data_list_offline:
            zone_offline.append(int(i))
        
        json_dict['data_list_offline']=zone_offline

        json_data=json.dumps(json_dict)
        print json_data
        return HttpResponse(json_data)
       
    return render(request,'threeapps.html')
