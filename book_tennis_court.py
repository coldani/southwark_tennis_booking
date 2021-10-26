'''
This program tries to book a tennis court slot in either Southwark Park or Tanner
Street Park.
It uses functions defined in helper.py and constants defined in constants.py.

usage: book_tennis_court.py [-h] [--date [DATE]] [--wait [WAIT]] [times]

positional arguments:
times:  {8:00,8:30,9:00,9:30,10:00,10:30,11:00,11:30,12:00,12:30,13:00,13:30,14:00,
14:30,15:00,15:30,16:00,16:30,17:00,17:30,18:00,18:30,19:00,19:30,20:00,20:30}
                        The times that the script will try to book

optional arguments:
  -h, --help            show this help message and exit
  --date [DATE], -d [DATE]
                        The date that the script will try to book. Can be a
                        date, in which case it needs to be in the form 'yyyy-
                        mm-dd', or an integer, in which case it will indicate
                        the day falling 'date' days in the future.
                        Defaults to 7 (i.e. the day falling one week in the future)
  --wait [WAIT], -w [WAIT]
                        The time that the script will wait until making the
                        booking. Can either be 'no' (if we want to book
                        immediately) or be expressed in 'hour:minute:second').
                        Defaults to '20:0:0' (8pm)
'''

import argparse
from datetime import datetime, timedelta
from helper import setup_driver, book
from constants import SOUTHWARK_PARK_IDS, TANNER_PARK_IDS, TANNER_URL, \
    SOUTHWARK_URL, EMAIL, PASSWORD

###### This section defines command line arguments and options ######
parser = argparse.ArgumentParser()
available_hours = [str(h) for h in range(8, 21)]
time_options = [hour + ':' + min for hour in available_hours for min in ['00', '30']]
parser.add_argument('times', nargs='+', choices=time_options,
                    help='The times that the script will try to book')

date_def = 7
date_help = \
"The date that the script will try to book. Can be a date, in which case it \
needs to be in the form 'yyyy-mm-dd', or an integer, in which case it will \
indicate the day falling 'date' days in the future. Defaults to 7 (i.e. the day \
falling one week in the future)"
parser.add_argument('--date', '-d', nargs='?', dest='date', help=date_help, default=date_def)

wait_def = "20:0:0"
wait_help = \
"The time that the script will wait until making the booking. Can either be \
'no' (if we want to book immediately) or be expressed in 'hour:minute:second'). \
Defaults to '20:0:0' (8pm)"
parser.add_argument('--wait', '-w', nargs='?', dest='wait', help=wait_help, default=wait_def)

args = parser.parse_args()
times = args.times
date = args.date
wait = args.wait

if len(date) == 1:
    date = (datetime.today() + timedelta(int(date))).strftime("%Y-%m-%d")
else:
    assert(len(date)==10), "Date must be in the form 'yyyy-mm-dd'"

if wait.lower() == 'no':
    wait = None
else:
    assert(len(wait.split(':'))==3),\
        "Wait time must be either 'no' or in the form 'hour:minute:second'"
    h, m, s = wait.split(':')
    wait = (int(h), int(m), int(s))

###### End of command line arguments section ######


driver = setup_driver()
login_details = (EMAIL, PASSWORD)

try:
    book(driver, TANNER_URL, login_details, TANNER_PARK_IDS, date,
         times, wait=wait)
    book(driver, SOUTHWARK_URL, login_details, SOUTHWARK_PARK_IDS, date,
         times, wait=wait)

except Exception as e:
    print(e)

finally:
    driver.close()
