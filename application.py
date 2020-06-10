import json
import decimal
import sys
from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request
from flask import send_file
from flask import Response, make_response

from flask_cors import CORS
from io import BytesIO
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException
from MPAPI_GPX_classes import *

#use this to return the JSON string to the screen
def get_JSON(item):
	return app.response_class(json.dumps(item,cls=DecimalEncoder), content_type='application/json')

application = Flask(__name__)
#cors = CORS(app, resources={r"/*": {"origins": "*"}})
mpapi_gpx = MPAPI_GPX()


@application.route('/', methods=['GET', 'POST'])
def show_login():
	
	if request.method == 'POST':
		output = mpapi_gpx.getMP_GPX(request.form['username'],request.form['secret_key'])
		resp = make_response(output)
		resp.headers['Content-Type'] = 'text/xml;charset=UTF-8'
		resp.headers['Content-Disposition'] = 'attachment;filename=todos.gpx'
		return resp
			
	return render_template('main.html')
		
@application.errorhandler(403)
def page_not_found(error):
	return render_template('main.html', 'Access Denied')

@application.errorhandler(500)
def page_not_found(error):
	return render_template('main.html', 'Oops...')


if __name__ == '__main__':
	application.debug = True
	application.run()