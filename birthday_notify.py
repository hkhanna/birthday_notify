import os
import sys
import json
from urllib import request
from datetime import datetime as dt
import logging
import traceback

import env_vars

log = logging.getLogger(__name__) # TODO: have logging go somewhere useful

# Uncaught Exception Logging
def uncaught_exception_handler(*exc_info):
    exc_text = "".join(traceback.format_exception(*exc_info))
    log.error(f"Uncaught exception: {exc_text}")
sys.excepthook = uncaught_exception_handler

env_vars.load_file(".env")  # TODO: reference current directory
airtable_base_id, airtable_key, ifttt_maker_trigger, ifttt_key = env_vars.get_required(
    ["AIRTABLE_BASE_ID", "AIRTABLE_KEY", "IFTTT_MAKER_TRIGGER", "IFTTT_KEY"]
)

res = request.urlopen(
    f"https://api.airtable.com/v0/{airtable_base_id}/People?filterByFormula={{Birthday}}&api_key={airtable_key}"
)
records = json.loads(res.read())["records"]

today_bdays = []
for r in records:
    bday = dt.strptime(r["fields"]["Birthday"], "%Y-%m-%d").date()
    upcoming_bday = bday.replace(year=dt.now().year)

    # If the month and year are in the past, the upcoming birthday is the following year.
    if upcoming_bday < dt.now().date():
        upcoming_bday = upcoming_bday.replace(year=dt.now().year + 1)

    if upcoming_bday == dt.now().date():
        # Add the person to a list of names
        todays_bdays.append(r["fields"]["Name"])

bday_str = ", ".join(today_bdays)

# Launch IFTTT Notification with full list of names
if len(today_bdays) != 0:
    log.info(f"{len(today_bdays)} birthdays today: {bday_str}")
    res2 = request.urlopen(
        f"https://maker.ifttt.com/trigger/{ifttt_maker_trigger}/with/key/{ifttt_key}?value1={bday_str}"
    )
else:
    log.info("0 birthdays today")
