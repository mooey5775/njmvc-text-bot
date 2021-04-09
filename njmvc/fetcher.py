import time
import requests
from datetime import datetime

from njmvc.constants import FETCH_INTERVAL, APPOINTMENT_ID, LOCATIONS

DATE_FORMAT = "Next Available: %m/%d/%Y %I:%M %p"

ENDPOINT = "https://telegov.njportal.com/njmvc/CustomerCreateAppointments/GetNextAvailableDate"

def get_next_available(apt_id, loc_id):
    params = {
        'appointmentTypeId': apt_id,
        'locationId': loc_id
    }

    
    try:
        resp = requests.get(url=ENDPOINT, params=params)
    except:
        print("[WARN] Some exception occured when making request")
        return None

    if resp.status_code != 200:
        # oops, request failure
        print(f"[WARN] Request failed with status {resp.status_code}")
        return None

    next_apt = resp.json()

    if 'next' not in next_apt:
        return None

    if next_apt['next'] == "No Appointments Available":
        return None

    try:
        avail_date = datetime.strptime(next_apt['next'], DATE_FORMAT)
    except:
        # I don't care what errors this throws
        # The show must go on
        # Phil Murphy is not going to wait
        return None

    return avail_date

def get_all_appointments():
    appts = {}

    for location in LOCATIONS:
        apt_date = get_next_available(APPOINTMENT_ID, LOCATIONS[location])
        if apt_date is None:
            continue

        appts[location] = apt_date
        time.sleep(FETCH_INTERVAL / 1000)

    return appts
