# GPX Generator by Ridgeline Analytics

## Setup Steps

1) Install Python. https://www.python.org/downloads/
   1) You probably want to find your OS prefered process for installing python.
   2) e.g. Ubuntu: `sudo apt install python3.8`
2) Install PIP. https://pip.pypa.io/en/stable/installing/
   1) Again you'll want to find your OS preferred installation. 
   2) e.g. Ubuntu: `sudo apt install python3-pip` 
3) Install dependencies.
   1) `pip3 install click gpxpy itsdangerous jinja2 markupsafe simplejson pymemcache six werkzeug`

## Developing the Service

1) Start by running the service
   1) Tell flask where the app is; `export FLASK_APP=application.py`
   2) Start the web server; `flask run`
   3) Load the app in your browser; `http://127.0.0.1:5000`