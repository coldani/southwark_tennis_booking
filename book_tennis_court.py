'''
This program tries to book a slot in either Southwark Park or Tanner Street Park.
It uses functions defined in helper.py and constants defined in constants.py
'''

from datetime import datetime, timedelta
from helper import setup_driver, sign_in, get_booking_page, is_slot_available, \
    book_slot, wait_until
from constants import SOUTHWARK_PARK_IDS, TANNER_PARK_IDS, TANNER_URL, \
    SOUTHWARK_URL, EMAIL, PASSWORD

debug = False
driver = setup_driver()
start_hour_list = [16]
day = (datetime.today() + timedelta(7)).strftime("%Y-%m-%d")


### DEBUG ###
debug = True
start_hour_list = [15]
day = datetime(2021, 10, 25).strftime('%Y-%m-%d')
### END DEBUG ###

login_details = (EMAIL, PASSWORD)
wait_time = (20, 0, 0)


def book(driver, venue_url, login_details, venue_ids, day, start_hour_list,
         wait=None, full_hour_only=False, verbose=0):
    '''
    This function tries to book a slot in the selected venue for the day and
    times(s) specified, by iterating over all courts and over all specified times.
    Once a booking is successful, the function exits.

    Parameters:
    -> driver: an instance of selenium webdriver
    -> venue_url: string, url of the venue main booking page
    -> login_details: tuple or list, with email in position 0 and password in position 1
    -court_ids: dictionary.
            keys: court label (e.g. court_1, court_2)
            value: string, the IDs of each court. These differ from each venue
    -day: a string in the format 'YYYY-MM-DD'
    -start_hour_list: a list with the hours we want to try and book for
    -wait: either None (then the function will execute immediately) or a
          tuple/list in the form (hour, minute, second). In this case, the scrip
          will first login into the booking page and will then stop execution
          until the time threshold has been passed. Useful to book 1 week in
          advance as the booking page will open at 20pm (in which case, the value
          should be (20, 0, 0)).
    -full_hour_only: boolean, if True it will book a slot only if 1 full hour is
                    available, if False it will also book any 30mins slot it can
                    find
    -verbose: either 0 or 1. If 1, it will print some information on the booking
            progress.
    '''

    email, password = login_details
    sign_in(driver, venue_url, email, password)
    if wait is not None:
        wait_until(wait[0], wait[1], wait[2])
    get_booking_page(driver, venue_url, day)
    for start_hour in start_hour_list:
        for start_min in [0, 30]:
            start_time = int(start_hour * 60 + start_min)
            court_id = is_slot_available(
                driver, start_time, day, venue_ids, full_hour_only, verbose)
            if court_id is None:
                pass
            else:
                is_booked = book_slot(driver, start_time, day, court_id, verbose)
            if is_booked==1:
                return


try:
    book(driver, TANNER_URL, login_details, TANNER_PARK_IDS, day,
         start_hour_list, wait=None, full_hour_only=False, verbose=1)
    book(driver, SOUTHWARK_URL, login_details, SOUTHWARK_PARK_IDS, day,
         start_hour_list, wait=None, full_hour_only=False, verbose=1)

except Exception as e:
    print(e)

finally:
    driver.close()
