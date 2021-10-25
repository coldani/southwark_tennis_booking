'''
This program tries to book a slot in either Southwark Park or Tanner Street Park.
It uses functions defined in helper.py and constants defined in constants.py
'''

from datetime import datetime, timedelta
from helper import setup_driver, book
from constants import SOUTHWARK_PARK_IDS, TANNER_PARK_IDS, TANNER_URL, \
    SOUTHWARK_URL, EMAIL, PASSWORD

debug = False
driver = setup_driver()
start_hour_list = [16]
day = (datetime.today() + timedelta(7)).strftime("%Y-%m-%d")


### DEBUG ###
debug = True
start_hour_list = [15]
day = datetime(2021, 10, 26).strftime('%Y-%m-%d')
### END DEBUG ###

wait_time = (20, 0, 0)

login_details = (EMAIL, PASSWORD)
try:
    book(driver, TANNER_URL, login_details, TANNER_PARK_IDS, day,
         start_hour_list, wait=None, full_hour_only=False, verbose=1)
    book(driver, SOUTHWARK_URL, login_details, SOUTHWARK_PARK_IDS, day,
         start_hour_list, wait=None, full_hour_only=False, verbose=1)

except Exception as e:
    print(e)

finally:
    driver.close()
