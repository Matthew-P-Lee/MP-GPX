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

app = Flask(__name__)
app.secret_key = b'_5#ydhhL"F4Qewaxec]/'

mpapi_gpx = MPAPI_GPX()

API_LIMIT=50
CACHE_CLIENT_ENDPOINT = 'gpx-cache.r6bmze.cfg.use2.cache.amazonaws.com'

if app.env == 'development':
	CACHE_CLIENT_ENDPOINT = 'localhost'

CACHE_PORT = 11211
CACHE_EXPIRE = 10800

MSG_API_EXCEEDED = 'The API limit has been reached. Try again later.'
MSG_PROFILE_NOT_FOUND = 'Profile not found.'
MSG_404 = 'Page not found.'
MSG_500 = 'Well that didn\'t seem to work.'
MSG_INVALID_API_URL = 'The API call failed.'
MSG_PROFILE_FOUND = 'Found profile!'
GPX_FILENAME = 'todos.gpx'

#helper to return a JSON object as an HTTP response
def get_JSON(item):
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

#Increments the API request count, stores it in cache and returns the current count
def set_api_throttle():
	
	client = Client((CACHE_CLIENT_ENDPOINT, CACHE_PORT))	
	result = client.get('daily_requests')
		
	if (result):
		result = int(result) + 1	
	else:
		result = 1
			
	client.set('daily_requests',result, expire=CACHE_EXPIRE)
	
	return result

#returns true if the next request will exceed the MountainProject API limit
def get_api_throttle():
	is_throttled = 0
	
	#memecached
	client = Client((CACHE_CLIENT_ENDPOINT, CACHE_PORT))	
	result = client.get('daily_requests')
			
	if (result):
		result = int(result)
		if (result >= API_LIMIT):
			is_throttled = 1
		
	return is_throttled
		
#main screen
@app.route('/', methods=['GET', 'POST'])
def show_form():
	error = None
	is_throttled = get_api_throttle() 
	
	if request.method == 'POST' and is_throttled == 0:       
		try:
			profile = mpapi_gpx.getMP_Profile(request.form['username'])	
			set_api_throttle()
		except(http.client.InvalidURL) as error:
			error=MSG_INVALID_API_URL
			
		if (profile):	
			flash(MSG_PROFILE_FOUND)
			return render_template('main.html',username=request.form['username'],profile=profile)
		else:
			error=MSG_PROFILE_NOT_FOUND		
	else:
		if is_throttled:
			error=MSG_API_EXCEEDED
			
	return render_template('main.html', error=error)
		
@app.route('/downloads/<string:username>', methods=['GET', 'POST'])
def download(username):
	if get_api_throttle() == 0:		
		output = mpapi_gpx.getMP_GPX(username)
		set_api_throttle() 
		resp = make_response(output)
		resp.headers['Content-Type'] = 'text/xml;charset=UTF-8'
		resp.headers['Content-Disposition'] = 'attachment;filename=' + GPX_FILENAME
		return resp
	else:
		return render_template('main.html', error=MSG_API_EXCEEDED)
	
@app.errorhandler(404)
def page_not_found(error):
	return render_template('main.html',error=MSG_404)

@app.errorhandler(500)
def catch_all(error):
	return render_template('main.html', error=MSG_500)

@app.template_filter('formatdatetime')
def format_datetime(value, format="%d %b %Y %I:%M %p"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)

if __name__ == '__main__':
	app.run()