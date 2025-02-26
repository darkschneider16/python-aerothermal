"""Script to send i-DE metrics to Zabbix"""

import time
import argparse
import configparser
import sys
import csv
from datetime import datetime, timedelta

from iber import Iber
from exception import LoginException, ResponseException, NoResponseException

# Command line arguments
parser = argparse.ArgumentParser(prog='month_iber.py')
parser.add_argument("credentials", type=str,
                    help="file containing the i-DE credentials")
parser.add_argument("-y", "--year", type=str,
                    help="year you want to ask (format: YYYY)")
parser.add_argument("-m", "--month", type=str,
                    help="month you want to ask (format: MM)")
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

# We need to get start day and we save it
start = datetime.today()
if args.year and args.month:
    try:
        start = datetime.strptime('01-' + f'{args.month:02}' + '-' + str(args.year), '%d-%m-%Y')
    except ValueError:
        sys.exit('Month to treat format error')

# We need to get end day and we save it
end = (start.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)

try:
    consumo = connection.consumption(start, end)
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

print('Lecturas: ' + str(len(consumo)))

# CSV part
csv_data = [["watts", "date", "timestamp"]]
HOUR = 0
day_timestamp = start
for i,v in enumerate(consumo):
    timestamp = time.mktime((datetime.combine(day_timestamp, datetime.min.time())
                             + timedelta(hours=HOUR + 1)).timetuple())
    line = [consumo[i], datetime.fromtimestamp(timestamp), timestamp]
    csv_data.append(line)
    if HOUR == 23:
        HOUR = 0
        day_timestamp = day_timestamp + timedelta(days=1)
    else:
        HOUR = HOUR + 1

FILENAME = 'consumo_luz_' + str(args.year) + '_' + f'{args.month:02}' + '.csv'
with open(FILENAME, mode='w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerows(csv_data)
