import time

from datetime import datetime
from twilio.rest import Client

from njmvc import get_all_appointments, send_msg, send_removal_msg
from njmvc.constants import FETCH_INTERVAL
from secrets import ACCOUNT_SID, AUTH_TOKEN, FROM_NUMBER, TO_NUMBER

START_DATE = datetime(2021, 5, 18, 12, 0, 0)
END_DATE = datetime(2021, 5, 22, 23, 59, 59)

if __name__ == '__main__':
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    appts_notified = set()

    print("[INFO] Running...")

    while True:
        appts = get_all_appointments()

        for location, apt_date in appts.items():
            # only send notifications once
            if (location, apt_date) in appts_notified:
                continue
            appts_notified.add((location, apt_date))

            if START_DATE <= apt_date and apt_date <= END_DATE:
                print(f"[INFO] Found appointment at {location} on {apt_date}!")
                send_msg(client, location, apt_date, FROM_NUMBER, TO_NUMBER)

        # send removal notification messages
        for location, apt_date in list(appts_notified):
            if location not in appts or apt_date < appts[location]:
                # this means that the appointment was taken
                # or an SSL error occured
                # either way, doesn't hurt to send this
                # TODO: make some way to differentiate between this
                appts_notified.remove((location, apt_date))

                if START_DATE <= apt_date and apt_date <= END_DATE:
                    print(f"[INFO] Appointment at {location} on {apt_date} taken")
                    send_removal_msg(client, location, apt_date, FROM_NUMBER, TO_NUMBER)

        time.sleep(FETCH_INTERVAL / 1000)
