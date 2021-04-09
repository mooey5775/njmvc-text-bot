from njmvc.constants import APPOINTMENT_ID, LOCATIONS

URL_DATE_FORMAT = "%Y-%m-%d/%H%M"
SCHED_URL_BASE = "https://telegov.njportal.com/njmvc/AppointmentWizard"

MSG_DATE_FORMAT = "%b %d at %I:%M %p"

def get_apt_url(loc_id, apt_date):
    date_str = apt_date.strftime(URL_DATE_FORMAT)
    return f"{SCHED_URL_BASE}/{APPOINTMENT_ID}/{loc_id}/{date_str}"

def send_msg(client, loc_name, apt_date, from_num, to_num):
    apt_url = get_apt_url(LOCATIONS[loc_name], apt_date)

    body = f"APT AVAILABLE at {loc_name} on {apt_date.strftime(MSG_DATE_FORMAT)}\n{apt_url}"
    
    msg = client.messages.create(
        body=body,
        from_=from_num,
        to=to_num
    )

    # hopefully this gets sent, using status callbacks too annoying

def send_removal_msg(client, loc_name, apt_date, from_num, to_num):
    body = f"Someone took {loc_name} on {apt_date.strftime(MSG_DATE_FORMAT)}"

    msg = client.messages.create(
        body=body,
        from_=from_num,
        to=to_num
    )
    