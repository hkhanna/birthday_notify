# Overview
This is a set of lightweight personal scripts. The individual scripts are intended to be called via cron job. 

These scripts are intended to be used with python3 but without the deployment complexities of a virtual environment. Therefore, a requirement of this project is that I avoid any dependencies other than the standard library.

If I need a web server, I should use something like bottle.py. For now, though, these scripts are called by cron jobs.

These scripts may interact with the following third-party services:
- Airtable
- IFTTT

# birthday_notify.py
This script polls my Airtable CRM for today's birthdays and sends my phone a push notification (via IFTTT) if someone's birthday is today. 

## Installation birthday_notify.py - TODO
1. IFTTT setup. Trigger: birthday_morning. Maker -> Notification. Need android installed. 
2. On deployment VPS, ...
3. Crontab entry ...

## Deployment birthday_notify.py - TODO
1. Run `python -m unittest`.
2. Push to GitHub: `git push -u origin master`.
3. Push to deployment VPS: `git push -u deploy master`. At the normal daily time (specified in your crontab), you should get an IFTTT notification of any birthdays as well as a notification that the deploy was successful. 