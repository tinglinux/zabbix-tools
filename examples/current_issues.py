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

# Get a list of all issues (AKA tripped triggers)
triggers = zapi.trigger.get(only_true=1,
    skipDependent=1,
    monitored=1,
    active=1,
    output='extend',
    expandDescription=1,
    expandData='host',
)

# Do another query to find out which issues are Unacknowledged
unack_triggers = zapi.trigger.get(only_true=1,
    skipDependent=1,
    monitored=1,
    active=1,
    output='extend',
    expandDescription=1,
    expandData='host',
    withLastEventUnacknowledged=1,
)
unack_trigger_ids = [t['triggerid'] for t in unack_triggers]
print(unack_triggers)
print(unack_trigger_ids)
for t in triggers:
    t['unacknowledged'] = True if t['triggerid'] in unack_trigger_ids\
    else False

# Print a list containing only "tripped" triggers
for t in triggers:
    if int(t['value']) == 1:
        print("{0} - {1} {2}".format(
            t['host'],
            t['description'],
            '(Unack)' if t['unacknowledged'] else '')
        )
