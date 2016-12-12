import json
from pyicloud import PyiCloudService
import geopy 


# give a user a "location" which is one of the 12 hands of the clock 

class User:

	def __init__(self, profile_json):
		profile = json.loads(profile_json)
		self.name = profile['name']
		self.api = PyiCloudService(profile['username'], profile['password'])
		self.iphone = self.api.devices[profile['device_num']]
		locs = profile['locations']
		self.work = self.setup_work(locs['work'])
		self.home = self.setup_home(locs['home'])

	def get_location(self):
		return self.iphone.location()

	# todo: use work name to get gps coordinate
	def setup_work(self, work_addr):
		pass 

	# todo: use home address to get gps coordinates 
	def setup_home(self, home_addr):
		pass

