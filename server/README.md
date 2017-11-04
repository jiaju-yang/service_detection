### Initialize flask app
```shell
cd <project root>/server
virtualenv env
source env/bin/activate
pip install -r requirements.txt
export FLASK_APP=manage.py
export FLASK_CONFIG=prod    # Production server
export FLASK_CONFIG=dev     # Development server
```
### Initialize database
```shell
flask init
```
### Create an administrator
```shell
flask set_admin --username <username> --password <password> --sign <anything> --tip What\'s\ your\ sign?
```
### Start server
```shell
flask run
```
### Config supervisor, nginx and uwsgi
```shell
sudo ln -s /home/psyche/services/service_detection/server/nginx.conf /etc/nginx/sites-enabled/service_detection.conf
sudo ln -s /home/psyche/services/service_detection/server/supervisor.conf /etc/supervisor/conf.d/service_detection.conf
```