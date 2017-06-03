chown -R devops /srv/logs/

su -m devops -c "celery worker -A dwn  -l info -f /srv/logs/celery/celery.log"