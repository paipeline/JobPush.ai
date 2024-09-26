#!/bin/bash
crontab -l > current_cron
sed -i '/job_fetch.py/d' current_cron
crontab current_cron
rm current_cron
echo "Cron jobs for job_fetch.py have been removed."