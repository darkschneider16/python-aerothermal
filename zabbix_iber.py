"""Script to send i-DE metrics to Zabbix"""

import time
import argparse
import configparser
import sys
from datetime import date, datetime, timedelta
from zabbix_utils import ItemValue, Sender

from iber import Iber
from exception import LoginException, ResponseException, NoResponseException

HOST = 'Zabbix metrics'

# Command line arguments
parser = argparse.ArgumentParser(prog='zabbix_iber.py')
parser.add_argument("credentials", type=str,
                    help="file containing the i-DE credentials")
parser.add_argument("-d", "--day", type=str,
                    help="day you want to ask (format: DD-MM-YYYY)")
args = parser.parse_args()

# Credentials treatment
config = configparser.ConfigParser()
config.read(args.credentials)

# i-DE part
connection = Iber()
try:
    connection.login(config['i-DE']['User'], config['i-DE']['Password'])
except LoginException:
    print('Login error')
except ResponseException:
    print('Response not OK')
else:
    print('Login OK')

# If we need to treat some day we save it
if args.day:
    try:
        day = datetime.strptime(args.day, '%d-%m-%Y')
    except ValueError:
        sys.exit('Day to treat format error')
else:
    day = date.today()
the_day_before = day - timedelta(days=1)

try:
    consumo = connection.consumption_day(the_day_before, day)
    if not consumo:
        print('Returned an empty list of consumptions')
except ResponseException:
    print('Response is not OK')
except NoResponseException:
    print('No response from i-DE')
else:
    print('Response OK')

try:
    connection.logout()
except ResponseException:
    print('Response is not OK to logout')
except NoResponseException:
    print('No response from i-DE to logout')
else:
    print('Logout OK')

# Zabbix part
items = []
HOUR = 0
if args.day:
    consumo = consumo[-24:]
print(consumo)
for watts in consumo:
    if args.day:
        day_timestamp = day
    else:
        day_timestamp = the_day_before
    timestamp = time.mktime((datetime.combine(day_timestamp, datetime.min.time())
                             + timedelta(hours=HOUR + 1)).timetuple())
    item = ItemValue(HOST, 'ide.hourly.consumption', consumo[HOUR], timestamp)
    items.append(item)
    HOUR = HOUR + 1
sender = Sender(server=config['zabbix']['Server'],
                port=config['zabbix']['Port'])
response = sender.send(items)

# Logging
print(response)
