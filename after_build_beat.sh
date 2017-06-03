chown -R devops /srv/logs/
chown -R devops /code/

su -m devops -c "celery beat -A dwn -s /srv/logs/celery/db  -f /srv/logs/celery/celery.log  --loglevel=INFO"