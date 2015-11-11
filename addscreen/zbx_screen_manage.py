#!/usr/bin/env python
#coding:utf-8

from getpass import getpass
from pyzabbix import ZabbixAPI
import ConfigParser
import sys
import optparse
import argparse

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

def screen_update(screenid,screenname):
    zapi.screen.update(
        screenid=screenid,
        name=screenname
    )

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
elif args.screen.exist :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        print("this screen name exist")
    else :
        print("no this screen")
elif args.get.screen :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        response=screen_get(screen_name)
        print(response)
    else :
        print("this screen is not exist")
elif args.update.screen :
    screen_name=raw_input("please input the screen name:")
    status=screen_exist(screen_name)
    if status:
        screenid=screen_get(screen_name)[0]['screenid']
        screen_update(screenid,screen_name)
        print("update success")
    else :
        print("this screen is not exist")






