#!/usr/bin/env bash
# Deploy server app
cd /home/psyche/services/service_detection/server/
echo '[-] Installing pip dependencies...'
virtualenv env
source env/bin/activate
pip install -r requirements.txt
echo '[-] Installed pip dependencies'
echo '[-] Migrating database...'
export FLASK_APP=manage.py
export FLASK_CONFIG=prod
flask db migrate
flask db upgrade
echo '[-] Migrated database'
sudo ln -sf /home/psyche/services/service_detection/server/nginx.conf /etc/nginx/sites-enabled/service_detection.conf
sudo ln -sf /home/psyche/services/service_detection/server/supervisor.conf /etc/supervisor/conf.d/service_detection.conf
echo '[-] Configurated nginx and supervisor'
sudo service supervisor restart
sudo service nginx restart
echo '[-] Deploy successfully'