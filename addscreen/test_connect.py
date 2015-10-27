
#_*_ coding:utf-8 _*_
from getpass import getpass
from pyzabbix import ZabbixAPI
import ConfigParser
import sys

config = ConfigParser.ConfigParser()
with open("../conf/default.conf","rw") as cfgfile:
    config.readfp(cfgfile)
ZABBIX_SERVER = config.get("sign","url")
USER = config.get("sign","user")
PASSWORD = config.get("sign","password")

zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('%s'%(USER), '%s'%(PASSWORD))

#获取hostid
def get_hostids():
    host_list = open('host_list.txt','r')
    host_id_list = []
    for host_name in host_list.readlines():
        host_name = host_name.strip('\n')
        print(host_name)
        host_info=zapi.host.get(
            output='extend',
            filter={'host':'%s'%(host_name)}
        )
        host_id_list.append([t['hostid'] for t in host_info])
    host_list.close()
    return host_id_list

#获取graphid
def get_graphids(graph_name):
    graph_name = graph_name
    graph_id_list = []
    for host_ids in host_id_list:
        host_id = host_ids[0]
        #   print(host_id)
        graph_info=zapi.graph.get(
            output='extend',
            hostids=host_id,
            filter={'name':'%s'%(graph_name) }
        )
        #   print(graph_info)
        graph_id_list.append([t['graphid'] for t in graph_info])
    return graph_id_list

#create a screen ,return the screenids
def create_screen(screen_name,h=3,v=2):
    screen_info=zapi.screen.create(
        name=screen_name,
        hsize=h,
        vsize=v
    )
    screen_id=screen_info['screenids']
    return screen_id

def screen_exist(screen_name):
    exist_judge=zapi.screen.exists(
        name=screen_name
    )
    return exist_judge

#batch add screen_items to screen
def create_screen_item(screen_name,h=3,v=2,resourcetype=0,height=100,width=350):
    i=0
    list = open("host_list.txt")
    count = len(list.readlines())
    list.close()
    screen_id=create_screen(screen_name,h,v)
    for xx in range(0,v):
        for yy in range(0,h):
            zapi.screenitem.create(
                screenid=screen_id[0],
                resourcetype=resourcetype,
                resourceid=graph_id_list[i][0],
                x=yy,
                y=xx,
                height=height,
                width=width
            )
            if i < count-1:
                i +=1
            else:
                break
    return "\nExecute successfully"

screen_name = raw_input("please input you want to create screen name:\n")
if screen_exist(screen_name):
    print("screen name is exist")
    print("please rename your screen_name")
else:
    graph_name = raw_input("please input the graph name:\n")
    h = input("hsize:\n")
    v = input("vsize:\n")
    host_id_list=get_hostids()
    graph_id_list=get_graphids(graph_name)
    response=create_screen_item(screen_name,h,v)
    print(response)