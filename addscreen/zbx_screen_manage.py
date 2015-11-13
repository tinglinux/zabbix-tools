#!/usr/bin/env python
#coding:utf-8

from getpass import getpass
from pyzabbix import ZabbixAPI
import ConfigParser
import sys
import optparse
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server",metavar="url",help="zabbix server url")
parser.add_argument("-u","--user",metavar="username",help="zabbix user name")
parser.add_argument("-p","--password",metavar="password",help="zabbix user login password")
parser.add_argument("--create",dest="create_screen",action="store_true",help="create a screen")
parser.add_argument("--delete",dest="delete_screen",action="store_true",help="delete a screen")
parser.add_argument("--exist",dest="screen_exist",action="store_true",help="judge a screen exists or not")
parser.add_argument("--get",dest="get_screen",action="store_true",help="get a screen information")
parser.add_argument("--update",dest="update_screen",action="store_true",help="update a screen information")
parser.add_argument("--create-item",dest="create_item",action="store_true",help="add items to a screen")
parser.add_argument("--detele-item",dest="delete_item",action="store_true",help="delete items from a screen")
parser.add_argument("--get-item",dest="get_item",action="store_true",help="get items info from a screen")
parser.add_argument("--isreadable-item",dest="isreadable_item",action="store_true",help="judge the item isreadable")
parser.add_argument("--iswriteable-item",dest="iswriteable_item",action="store_true",help="judge the item iswriteable")
parser.add_argument("--update-item",dest="update_item",action="store_true",help="update item's info")
parser.add_argument("--updatebyposition-item",dest="updatebyposition_item",action="store_true",help="update item by the item's position")
parser.add_argument("--file",dest="filename",help="host list file")
args = parser.parse_args()

if not args.server:
    args.server=raw_input("server url(http://localhost):")
if not args.user:
    args.user=raw_input("Username:")
if not args.password:
    args.password=getpass()

ZABBIX_SERVER = args.server
USER = args.user
PASSWORD = args.password
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('%s'%(USER), '%s'%(PASSWORD))

def create_screen(screen_name,h=3,v=2):
    screen_info=zapi.screen.create(
        name=screen_name,
        hsize=h,
        vsize=v
    )
    screen_id=screen_info['screenids']
    return screen_id

def delete_screen(screenid):
    zapi.screen.delete(screenid)

def screen_exist(screen_name):
    exist_judge=zapi.screen.exists(
        name=screen_name
    )
    return exist_judge

def screen_get(screen_name,output="extend",selectScreenItems="extend"):
    response=zapi.screen.get(
        filter={'name':'%s'%(screen_name)},
        output=output,
        selectScreenItems=selectScreenItems
    )
    return response

def screen_update(json_name):
    zapi.screen.update(
        json_name
    )

def get_hostids(filename):
    if os.path.exists(filename):
        host_list = open('%s'%(filename),'r')
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
    else :
        hostname=filename
        host_info=zapi.host.get(
            output='extend',
            filter={'host':'%s'%(hostname)}
        )
        print(host_info[0]['hostid'])
        host_id=host_info[0]['hostid']
        return host_id

def get_graphids(graph_name,host_id_list):
    graph_name = graph_name
    graph_id_list = []
    print(host_id_list)
    for host_ids in host_id_list:
        host_id = host_ids[0]
        print(host_id)
        graph_info=zapi.graph.get(
            output='extend',
            hostids=host_id,
            filter={'name':'%s'%(graph_name) }
        )
        #   print(graph_info)
        graph_id_list.append([t['graphid'] for t in graph_info])
    return graph_id_list

def create_screen_item(filename,screen_name,graph_list_id,h=3,v=2,resourcetype=0,height=100,width=350):
    i=0
    if os.path.exists(filename):
        list = open("%s"%(filename))
        count = len(list.readlines())
        list.close()
        graph_id_list=graph_list_id
        screen_id=screen_get(screen_name)[0]['screenid']
        print(screen_id)
        print(count)
        print(graph_id_list)
        for xx in range(0,v):
            for yy in range(0,h):
                zapi.screenitem.create(
                    screenid=screen_id,
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
    else:
        graph_id_list=graph_list_id
        screen_id=screen_get(screen_name)[0]['screenid']
        print(screen_id)
        print(graph_id_list)
        yy=h
        xx=v
        zapi.screenitem.create(
            screenid=screen_id,
            resourcetype=resourcetype,
            resourceid=graph_id_list,
            x=yy,
            y=xx,
            height=height,
            width=width
        )
        return "\nExecute successfully"

if args.create_screen :
    print("now we will create a screen:")
    screen_name=raw_input("please input the screen name which you want to create:")
    status=screen_exist(screen_name)
    if status:
        print(screen_name,"is exist")
    else :
        column=input("please input the screen high size:")
        row=input("please input the screen width size:")
        response=create_screen(screen_name,column,row)
        print("create sucess and the screenid is %s"%response[0])
elif args.delete_screen:
    print("now we will delete a screen:")
    screen_name=raw_input("please input the screen name which you want to delete:")
    status=screen_exist(screen_name)
    if status:
        screenid=screen_get(screen_name)[0]['screenid']
        print(screenid)
        delete_screen(screenid)
        print("delete success")
    else:
        print("this screen name does't exist,please check your screen name")
elif args.screen_exist :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        print("this screen name exist")
    else :
        print("no this screen")
elif args.get_screen :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        response=screen_get(screen_name)
        print(response)
    else :
        print("this screen is not exist")
elif args.update_screen :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        screenid=screen_get(screen_name)[0]['screenid']
        json_name=raw_input("input a name you want change(json format):")
        screen_update(json_name)
        print("update success")
    else :
        print("this screen is not exist")
elif args.create_item :
    if args.filename:
        filename=args.filename
        host_id_list=get_hostids(filename)
        graph_name=raw_input("input the graph name:")
        screen_name=raw_input("input the screen name:")
        graph_id_list=get_graphids(graph_name,host_id_list)
        response=create_screen_item(filename,screen_name,graph_id_list,h=3,v=1,resourcetype=0,height=100,width=350)
        print(response)
    else:
        print("this file is not exist")
        hostname=raw_input("input hostname:")
        host_id=get_hostids(hostname)
        print(host_id)
        graph_name=raw_input("input the graph name:")
        screen_name=raw_input("input the screen name:")
        width=raw_input("this graph x place:")
        hight=raw_input("this graph y place:")
        source=raw_input("this graph sourcetype(0-9):")
        graph_info=zapi.graph.get(
            output='extend',
            hostids=host_id,
            filter={'name':'%s'%(graph_name) }
        )
        print(graph_info)
        graph_id_list=graph_info[0]['graphid']
        response=create_screen_item(hostname,screen_name,graph_id_list,h=width,v=hight,resourcetype=source,height=100,width=350)
        print(response)




