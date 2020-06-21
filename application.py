import json
import datetime
import http
import decimal
import sys
import tempfile

from flask import *
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from pymemcache.client.base import Client

from MPAPI_GPX_classes import *

#use this to return the JSON string to the screen
def get_JSON(item):
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

app = Flask(__name__)
app.secret_key = b'_5#ydhhL"F4Qewaxec]/'

mpapi_gpx = MPAPI_GPX()

API_LIMIT=250
CACHE_CLIENT_ENDPOINT = 'localhost'
#CACHE_CLIENT_ENDPOINT = 'gpx-cache.r6bmze.cfg.use2.cache.amazonaws.com'
CACHE_PORT = 11211

#adds one to the API request count and returns the current count
def set_api_throttle():
	
	client = Client((CACHE_CLIENT_ENDPOINT, CACHE_PORT))	
	result = client.get('daily_requests')
		
	if (result):
		result = int(result) + 1	
	else:
		result = 1
			
	client.set('daily_requests',result, expire=10800)
	
	return result

#returns true if the next request will exceed the MountainProject API limit
def get_api_throttle():
	is_throttled = 0
	
	#memecached
	client = Client((CACHE_CLIENT_ENDPOINT, CACHE_PORT))	
	result = client.get('daily_requests')
			
	if (result):
		result = int(result)
		print(result)
		if (result >= API_LIMIT):
			is_throttled = 1
		
	return is_throttled
		
@app.route('/', methods=['GET', 'POST'])
def show_login():
	error = None
	is_throttled = get_api_throttle() 
	
	if request.method == 'POST' and is_throttled == 0:       
		try:
			profile = mpapi_gpx.getMP_Profile(request.form['username'])	
			set_api_throttle()
		except(http.client.InvalidURL) as error:
			return render_template('main.html',error=error)
			
		if (profile):	
			flash("Found Profile!")
			return render_template('main.html',username=request.form['username'],profile=profile)
		else:
			return render_template('main.html',error='Profile not found.')	
	else:
		if is_throttled:
			error = "The MountainProject API limit has been reached. Try again later."
			
		return render_template('main.html', error=error)
		
@app.route('/downloads/<string:username>', methods=['GET', 'POST'])
def download(username):
	output = mpapi_gpx.getMP_GPX(username)
	set_api_throttle() 
	resp = make_response(output)
	resp.headers['Content-Type'] = 'text/xml;charset=UTF-8'
	resp.headers['Content-Disposition'] = 'attachment;filename=todos.gpx'
	return resp
	
@app.errorhandler(404)
def page_not_found(error):
	return render_template('main.html',error='Page not found.')

@app.errorhandler(500)
def catch_all(error):
	return render_template('main.html', error='Well that didn\'t seem to work.')

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

if __name__ == '__main__':
	app.run()