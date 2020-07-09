'''
    File name: MPAPI_GPX_classes.py
    Author: Matthew Lee - matthew.lee@ridgeline-analytics.com
    Date created: 6/8/2020
    Date last modified: 6/8/2020
    Python Version: 3.7
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
		
	#return a Python obj from a JSON HTTP response
	def getMP_API(self,url):
		json_str = urllib.request.urlopen(url).read()
		if len(json_str) > 0:
			json_str = json.loads(json_str)
		
		return json_str
	
	#formatted Mountain Project API URL	
	def getMP_URL(self,mp_URL_base,mp_command,mp_URL_email):
		outstr = str.format("{0}/{1}?email={2}&key={3}",mp_URL_base,mp_command,mp_URL_email,self.mp_private_key)
		return outstr

	#gets a profile
	def getMP_Profile(self,mp_URL_email):
		#conditional load of the user profile
		profile_url = self.getMP_URL(self.mp_URL_base,'get-user',mp_URL_email)
		return self.getMP_API(profile_url)
	
	#queries the mountainproject to do list API
	def getToDos(self,mp_URL_email,pos):
		todos_url = self.getMP_URL(self.mp_URL_base,'get-to-dos',mp_URL_email)
		todos_url = str.format(todos_url + '&startPos=' + str(pos))
		return self.getMP_API(todos_url)
	
	#gets a list of routes from a list of route ids	
	def getRoutes(self,mp_URL_email,route_ids):
		routes_url = self.getMP_URL(self.mp_URL_base,'get-routes',mp_URL_email)
		routes_url = str.format("{0}&routeIds={1}",routes_url,route_ids)
		return self.getMP_API(routes_url)

	#lat=40.03&lon=-105.25&maxDistance=10&minDiff=5.6&maxDiff=5.10&key=112244155-faf71266e0e5a4f73c53cc5ef291800d	
	def getRoutesForLatLong(self,mp_URL_email,lat,long):
		routes_url = self.getMP_URL(self.mp_URL_base,'get-routes-for-lat-lon',mp_URL_email)
		routes_url = str.format("{0}&lat={1}&lon={2}&maxDistance=5&minDiff=5.6&maxDiff=5.10",routes_url,lat,long)
		return self.getMP_API(routes_url)
  		 

	#gets a GPX file for routes near a given user's lat / long
	def getMP_GPX_location(self,mp_URL_email,lat,long):

		gpxinstance = gpx.GPX()
		mp_routes = self.getRoutesForLatLong(mp_URL_email,lat,long)
		
		for route in mp_routes['routes']:
			gpxinstance.waypoints.append(
				gpx.GPXWaypoint(
					Decimal(str(route['latitude'])), 
					Decimal(str(route['longitude'])), 
					name=route['name'] + ' - ' + route['rating'],
					description=route['url']))
			
		return gpxinstance.to_xml()
		

	#returns a string of XML 
	def getMP_GPX(self,mp_URL_email):
		pos = 0
		gpxinstance = gpx.GPX()
		mp_todos = self.getToDos(mp_URL_email,pos)
	
		#requery the API if we've reached 200 and there's still something returned
		while (len(mp_todos['toDos']) > 0):
			
			if (pos > 0): #requery the API to get next 200 batch
				mp_todos = self.getToDos(mp_URL_email,pos)
				
			#get routes returns an array of integer route ids, make a string to pass to MP
			route_ids = ','.join(str(todo) for todo in mp_todos['toDos'])
			
			if len(route_ids) > 0:		
				mp_routes = self.getRoutes(mp_URL_email,route_ids)

				for route in mp_routes['routes']:
					pos += 1
		
					gpxinstance.waypoints.append(
						gpx.GPXWaypoint(
							Decimal(str(route['latitude'])), 
							Decimal(str(route['longitude'])), 
							name=route['name'] + ' - ' + route['rating'],
							description=route['url']))
			
		return gpxinstance.to_xml()
