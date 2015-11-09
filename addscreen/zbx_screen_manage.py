#!/usr/bin/env python
#coding:utf-8

from getpass import getpass
#from pyzabbix import ZabbixAPI
import ConfigParser
import sys
import optparse
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-s","--server",metavar="url",help="zabbix server url")
parser.add_argument("-u","--user",metavar="username",help="zabbix user name")
parser.add_argument("-p","--password",metavar="password",help="zabbix user login password")
parser.add_argument("--create",metavar="screenname",help="create a screen")
parser.add_argument("--delete",metavar="screenname",help="delete a screen")
parser.add_argument("--exist",metavar="screenname",help="judge a screen exists or not")
parser.add_argument("--get",metavar="screenname",help="get a screen information")
parser.add_argument("--update",dest="screenname",help="update a screen information")  //dest and matavar
args = parser.parse_args()
print args.square**2
print args.method**2