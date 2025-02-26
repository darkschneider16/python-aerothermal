"""Script to send i-DE metrics to Zabbix"""

import time
import argparse
import configparser
import csv
from datetime import date, datetime, timedelta
from zabbix_utils import ItemValue, Sender

from iber import Iber
from exception import LoginException, ResponseException, NoResponseException

HOST = 'Zabbix metrics'

# Command line arguments
parser = argparse.ArgumentParser(prog='zabbix_iber.py')
parser.add_argument("credentials", type=str,
                    help="file containing the i-DE credentials")
parser.add_argument("-f", "--file", type=str,
                    help="file containing readings in csv format")
args = parser.parse_args()

# Credentials treatment
config = configparser.ConfigParser()
config.read(args.credentials)

# CSV reading part
try:
    with open(args.file, encoding='utf-8', mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row['watts'] + ' -> ' + row['timestamp'])
except OSError:
    print('CSV File error')

# Zabbix part
# items = []
# HOUR = 0
# if args.day:
#     consumo = consumo[-24:]
# print(consumo)
# for watts in consumo:
#     if args.day:
#         day_timestamp = day
#     else:
#         day_timestamp = the_day_before
#     timestamp = time.mktime((datetime.combine(day_timestamp, datetime.min.time())
#                              + timedelta(hours=HOUR + 1)).timetuple())
#     item = ItemValue(HOST, 'ide.hourly.consumption', consumo[HOUR], timestamp)
#     items.append(item)
#     HOUR = HOUR + 1
# sender = Sender(server=config['zabbix']['Server'],
#                 port=config['zabbix']['Port'])
# response = sender.send(items)
