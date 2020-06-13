'''
    File name: MPAPI_GPX_Generator
    Author: Matthew Lee - matthew.lee@ridgeline-analytics.com
    Date created: 6/8/2020
    Date last modified: 6/8/2020
    Python Version: 3
    Description: A script that creates a GPX file from MountainProject todo lists.
'''

import urllib.request
import gpxpy.gpx as gpx
import simplejson as json
from decimal import *

class MPAPI_GPX:

	mp_URL_base='https://www.mountainproject.com/data'
	mp_private_key='112244155-faf71266e0e5a4f73c53cc5ef291800d'
	
	def __init__(self):
		return
		
	#function to return a Python obj from a JSON result via HTTP
	def getMP_API(self,url):
		json_str = urllib.request.urlopen(url).read()
		if len(json_str) > 0:
			json_str = json.loads(json_str)
		
		return json_str
	
	#formatted Mountain Project API URL	
	def getMP_URL(self,mp_URL_base,mp_command,mp_URL_email):
		return str.format("{0}/{1}?email={2}&key={3}",mp_URL_base,mp_command,mp_URL_email,self.mp_private_key)

	#gets a profile
	def getMP_Profile(self,mp_URL_email):
		#conditional load of the user profile
		profile_url = self.getMP_URL(self.mp_URL_base,'get-user',mp_URL_email)
		return self.getMP_API(profile_url)

	#returns a string of XML 
	def getMP_GPX(self,mp_URL_email):
		todos_url = self.getMP_URL(self.mp_URL_base,'get-to-dos',mp_URL_email)
		mp_todos = self.getMP_API(todos_url)

		#get routes returns an array of integer route Ids, make a string to pass to MP
		route_ids = ','.join(str(todo) for todo in mp_todos['toDos'])
	
		gpxinstance = gpx.GPX()

		if len(route_ids) > 0:		
			#return routes for the list of todos 
			routes_url = self.getMP_URL(self.mp_URL_base,'get-routes',mp_URL_email)
			routes_url = str.format("{0}&routeIds={1}",routes_url,route_ids)
			mp_routes = json_str = self.getMP_API(routes_url)

			for route in mp_routes['routes']:
				gpxinstance.waypoints.append(
					gpx.GPXWaypoint(
						Decimal(str(route['latitude'])), 
						Decimal(str(route['longitude'])), 
						name=route['name'] + ' - ' + route['rating'],
						description=route['url']))
	
		return gpxinstance.to_xml()
