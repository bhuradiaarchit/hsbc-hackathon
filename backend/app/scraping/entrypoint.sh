#!/bin/bash

export TZ=Asia/Kolkata

# Define the cron job
CRON_JOB="
30 14 * * * /usr/local/bin/python3 /app/main.py >> /var/log/scrape.log 2>&1
"

# Add cron job to the crontab
echo "$CRON_JOB" | crontab -

# Start the cron service in the foreground
exec cron -f