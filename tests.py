import unittest
import warnings
from MPAPI_GPX_classes import *


#testing for the API
class TestMPAPI_GPX(unittest.TestCase):
	MP_USER = 'matt@vistaseeker.com'	
	MP_TEST_ROUTE_ID = 105721759 #double crack at Joshua Tree ;-)
			
	def test_GetUser(self):
		profile = MPAPI_GPX().getMP_Profile(self.MP_USER)	
		#print(profile)
		self.assertTrue(profile)

	def test_GetToDos(self):
		todos = MPAPI_GPX().getToDos(self.MP_USER,0)
		#print(todos)
		self.assertTrue(todos)

	def test_GetRoutes(self):
		routes = MPAPI_GPX().getRoutes(self.MP_USER,self.MP_TEST_ROUTE_ID)
		#print(routes)
		self.assertTrue(routes)

if __name__ == '__main__':
    unittest.main()
