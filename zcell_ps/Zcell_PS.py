# -*- coding: utf-8 -*-  

import re
import time
import calendar
import datetime
import datetime as dt
import ConfigParser
import os
import sys
import psutil
import pykafka
from pykafka import KafkaClient
from pykafka.common import OffsetType
from pykafka.protocol import PartitionOffsetCommitRequest

#------------------------------------------------------------
def dir_find(begin_dir):
    
    if os.path.isdir(begin_dir):
        begin_list=os.listdir(begin_dir)
        for zcell_level in begin_list:
            searchobj=re.search(r'[A-Z]{1,4}[0-9]{7,8}',zcell_level)
            if searchobj!=None:
                zcell_module.append(searchobj.group())     
   

def log_find(log_str):
    """get the  number of online """
    log_list=os.listdir(log_str)
    for da_li in log_list:
        if now.year==int(da_li[:4]) and now.month==int(da_li[4:6]) and now.day==int(da_li[6:8]):
            log_str=log_str+"\\"+da_li+"\\"+"Plugin_CheckDeviceStates.log"
            if os.path.exists(log_str):
                with open(log_str) as f:
                    f.seek(-10,2)
                    str_last=f.read(10)
                    f.close()
                    return re.search(r'[0-9]+',str_last).group()   # the host number
            
            
def online_zcell(zcell_m,begin_dir):
    """get the online zcell and the module in zcell server """
    config = ConfigParser.ConfigParser()
    node_exe=[]   # exe file set
    node_exe_dir=[]
    is_online=[]  #  active module
    module_online=[]
    for item in zcell_m:
        start_up=begin_dir+"\\"+item   # \\"+"Startup.ini"
        log_li=os.listdir(start_up)
        for i in log_li:
            if re.search('.exe',i)!=None:
                node_exe.append(i)
                node_exe_dir.append(item)
       
    for p in psutil.process_iter():
        for item in node_exe:
            searchObj=re.search(item,str(p.name))
            if searchObj !=None:
                item_index=node_exe.index(item)
                
                is_online.append(node_exe_dir[item_index]) # is the exe file  ,mae the exe exists -----two
                module_online.append(searchObj.group()[:-4])  #  only one ==========
    return is_online,module_online

def kafka_producter(msg,topic):
    """kafka product is here"""
    
    with topic.get_sync_producer() as producer:
        producer.produce(msg)
def get_ini():
    """ config file """
    config = ConfigParser.ConfigParser()
    start_f=open("zcell_ps.ini","rb")
    config.readfp(start_f)
    host_cluster=config.get("global","ip")
    topic_cluster=config.get("global","topic")
    zcell_id=config.get("global","zcell_id")
    zcell_dir=config.get("global","dir")
    consumer_group=config.get("global","group")
    start_f.close()
    return host_cluster,topic_cluster,zcell_id,zcell_dir,consumer_group

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

def fetch_consumer_lag(client, topic_str, consumer_group):
    """Get raw lag data for a topic/consumer group """
    topic=client.topics[topic_str]  #    function output_topic_lag
    
    latest_offsets = fetch_offsets(client, topic, 'latest')
    consumer = topic.get_simple_consumer(consumer_group=consumer_group,
                                         auto_start=False)
    current_offsets = consumer.fetch_offsets()
    return {p_id: (latest_offsets[p_id].offset[0], res.offset) for p_id, res in current_offsets}

def output_topic_lag(client,topic):
    """topic is string """
    tmp_topic=client.topics[topic]
    return tmp_topic


    
if __name__=="__main__":
    print "+++++++++++++++++++++++++++"+u"请不要关闭".encode("GBK")+"+++++++++++++++++++++++\n"
    print "+++++++++++++++++++++++++++"+u"程序运行中".encode("GBK")+"+++++++++++++++++++++++\n"
    print "+++++++++++++++++++"+u"若不小心关闭，请点击桌面快捷方式".encode("GBK")+"+++++++++++++++++\n"
    print "++++++++++++++++++++++++++"+u"快捷图标为ZCELL_log"+"+++++++++++++++++++++++++++"
    

    now=datetime.datetime.now() 
    delta_minutes=datetime.timedelta(minutes=1)
    delta_time=now+delta_minutes
    # kafka  config
    host_cluster,topic_cluster,zcell_id,zcell_dir,group=get_ini()
    begin_dir=zcell_dir                              # read the config
    client = KafkaClient(hosts=host_cluster)        ## read the  zcell_ps  config
    topic=client.topics[topic_cluster]           ##  read the  zcell_ps  config
    while True:
        dict={}
        dict['zcell_id']=zcell_id         # in config file 
        now=datetime.datetime.now()
        if now >= delta_time:
            delta_time+=delta_minutes
            # restart must ini it again
            
            zcell_module=[]
            is_active_number=[]
            lastest_offset_list=[]
            current_offset_list=[]
            lag_list=[]
            number=0
            
            
            dir_find(begin_dir)                  #  the function get zcell (all module )
            #dict["zcell_module"]=zcell_module
            is_active,module_active=online_zcell(zcell_module,begin_dir)   # list of module is running---- is_active dir
            dict["is_active"]=is_active
            #dict["module_active"]=module_active  # is for test only
            if is_active !=[]:
                for mo in is_active:
                    module_level=begin_dir+"\\"+mo+"\\"+"log"
                    
                    if re.search(r'V',mo):
                        pass
                    else:
                        num=log_find(module_level)    #  the function
                        is_active_number.append(num)
                        if num==None:
                            num=0
                        number+=int(num)
                        #tmp_topic=output_topic_lag(client,mo)  # the topic is for topic_lag
                             
                        
                        offset_lastest=fetch_consumer_lag(client,mo,mo)[0]  #return offset for lag
                        latest_offset=offset_lastest[0]
                        lastest_offset_list.append(latest_offset)
                        current_offset=offset_lastest[1]
                        current_offset_list.append(current_offset)
                        lag=latest_offset-current_offset
                        lag_list.append(lag)

                
                
                dict["date"]=delta_time
                dict["latest_offset"]=lastest_offset_list
                dict["current_offset"]=current_offset_list
                dict["lag"]=lag_list
                    
                    
                dict["is_active_number"]=is_active_number            # just for self use
                dict["host_number"]=number
                
                
                    
                kafka_producter(str(dict),topic)
                log_f=open("..\message.log","a")
                log_f.write(str(dict)+"\n")
                log_f.close()
                
            # host_num is the host in some module , here is the all module
            #kafka_producter(dict,topic)                # the kafka send  function
         
        
            
                
        
 
