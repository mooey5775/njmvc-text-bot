import time

from datetime import datetime
from twilio.rest import Client

from njmvc import get_all_appointments, send_msg
from njmvc.constants import FETCH_INTERVAL
from secrets import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER

START_DATE = datetime(2021, 5, 18, 12, 0, 0)
#END_DATE = datetime(2021, 5, 22, 23, 59, 59)
END_DATE = datetime(2021, 8, 1)

if __name__ == '__main__':
    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    while True:
        appts = get_all_appointments()

        for location, apt_date in appts.items():
            if START_DATE <= apt_date and apt_date <= END_DATE:
                print(f"[INFO] Found appointment at {location} on {apt_date}!")
                send_msg(client, location, apt_date, FROM_NUMBER, TO_NUMBER)

        time.sleep(FETCH_INTERVAL / 1000)
