# birthday_notify.py
This script polls my Airtable CRM for today's birthdays and sends my phone a push notification (via Pushover) if someone's birthday is today. 

This script is intended to be called via cron job. 

There are no dependencies other than the python3 standard library.

This script interacts with the following third-party services:
- Airtable
- Pushover

Logs go to `app.log` in the repo directory. 

## Installation birthday_notify.py 
1. Create a Pushover application. Make sure the Pushover application is installed on your phone.
2. Clone this repo onto the deployment VPS.
3. Copy .env_example to .env and set the appropriate environment variables. 
4. Add a crontab entry to run `birthday_notify.py` once a day in the morning.

## Update birthday_notify.py 
1. Push to GitHub: `git push -u origin master`.
2. From VPS, `git pull` the changes.