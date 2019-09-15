import os
import sys
import json
from urllib import request, parse
from datetime import datetime as dt
import logging
import traceback

current_path = os.path.dirname(os.path.abspath(__file__))
logging.basicConfig(
    filename=current_path + "/app.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s - [%(name)s] %(message)s",
)
log = logging.getLogger('birthday_notify')

import env_vars

# Uncaught Exception Logging
def uncaught_exception_handler(*exc_info):
    exc_text = "".join(traceback.format_exception(*exc_info))
    log.error("Uncaught exception: {}".format(exc_text))


sys.excepthook = uncaught_exception_handler

env_vars.load_file(current_path + "/.env")
airtable_base_id, airtable_key, ifttt_maker_trigger, ifttt_key = env_vars.get_required(
    ["AIRTABLE_BASE_ID", "AIRTABLE_KEY", "IFTTT_MAKER_TRIGGER", "IFTTT_KEY"]
)

res = request.urlopen(
    "https://api.airtable.com/v0/{}/People?filterByFormula={{Birthday}}&api_key={}".format(
        airtable_base_id, airtable_key
    )
)
records = json.loads(res.read().decode())["records"]

todays_bdays = []
for r in records:
    bday = dt.strptime(r["fields"]["Birthday"], "%Y-%m-%d").date()
    upcoming_bday = bday.replace(year=dt.now().year)

    # If the month and year are in the past, the upcoming birthday is the following year.
    if upcoming_bday < dt.now().date():
        upcoming_bday = upcoming_bday.replace(year=dt.now().year + 1)

    if upcoming_bday == dt.now().date():
        # Add the person to a list of names
        todays_bdays.append(r["fields"]["Name"])

bday_str = ", ".join(todays_bdays)

# Launch IFTTT Notification with full list of names
if len(todays_bdays) != 0:
    log.info("{} birthdays today: {}".format(len(todays_bdays), bday_str))
    encoded_bday_str = parse.quote(bday_str)
    res2 = request.urlopen(
        "https://maker.ifttt.com/trigger/{}/with/key/{}?value1={}".format(
            ifttt_maker_trigger, ifttt_key, encoded_bday_str
        )
    )
else:
    log.info("0 birthdays today")
