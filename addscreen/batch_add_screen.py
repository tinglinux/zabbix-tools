__author__ = 'tt'
from pyzabbix import ZabbixAPI,ZabbixAPIException
import  sys

'''set zabbix server login parameter'''
ZABBIX_SERVER = "http://192.168.142.99"
zapi = ZabbixAPI(ZABBIX_SERVER)
zapi.login('api','api123456')

screen = zapi.screen.create(
    name = "CPU utilization3",
    hsize = 3,
    vsize = 2
)
def lines(file):
    for line in file:
        yield line
def host_ids(file):
    host_id = []
    for line in lines(file):
        host_info = zapi.host.get(
            output = 'extend',
            filter = {'host':'%s'%(line)}
        )
        print(host_info)
        host_id.append(host_info[0]["hostid"])
for host_id in host_ids(sys.stdin):
    print(host_id)
print(screen)
print('screenids {0}',format(screen['screenids']))
