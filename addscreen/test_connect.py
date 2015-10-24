__author__ = 'tt'
"""
Shows a list of all current issues (AKA tripped triggers)
"""

from getpass import getpass
from pyzabbix import ZabbixAPI

# The hostname at which the Zabbix web interface is available
ZABBIX_SERVER = 'http://192.168.142.99'

zapi = ZabbixAPI(ZABBIX_SERVER)

# Login to the Zabbix API
zapi.login('api', 'api123456')

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
print(host_id_list)
graph_list = open('graph.txt','r')
graph_name = graph_list.readline().strip('\n')
graph_id_list = []
for host_ids in host_id_list:
    host_id = host_ids[0]
    print(host_id)
    graph_info=zapi.graph.get(
        output='extend',
        hostids=host_id,
        filter={'name':'%s'%(graph_name) }
    )
    print(graph_info)
    graph_id_list.append([t['graphid'] for t in graph_info])
print(graph_id_list)
def create_screen():
    screen_info=zapi.screen.create(
        name='publishing environment cpu ultilization',
        hsize=3,
        vsize=7
    )
    return screen_info
screen_info=create_screen()
#print(screen_info)
screen_id=screen_info['screenids']
#print(screen_id[0])
def create_screen_item():
    i=0
    for xx in range(0,7):
        for yy in range(0,3):
            zapi.screenitem.create(
                screenid=screen_id[0],
                resourcetype=0,
                resourceid=graph_id_list[i][0],
                x=yy,
                y=xx,
                height=100,
                width=350
            )
            if i < 19:
                i +=1
            else:
                break
    return "Execute successfully"
response=create_screen_item()
print(response)