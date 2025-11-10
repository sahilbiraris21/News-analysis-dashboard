#!/bin/sh

exec python3 /app/crawler/main.py &
# exec python3 /app/cron/wrapper.py &
exec python3 /app/app.py