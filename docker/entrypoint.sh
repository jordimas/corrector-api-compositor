#/bin/sh
cd srv/web/
mkdir -p /var/log/api-compositor/
gunicorn api-compositor:app -b 0.0.0.0:8000 --error-logfile /var/log/api-compositor/gnuicorn.log --workers=2
