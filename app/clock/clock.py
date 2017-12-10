from user import User 
import sys

class Clock:

	def __init__(self, jackie_profile):
		self.jackie = User(jackie_profile)
		self.users = [self.jackie]

	# returns a map of user -> location data 
	def get_all_locations(self):
		return {u.name: u.get_location() for u in self.users}



# just some bullshit for start up testing 

profile_1 = open(sys.argv[1]).read()
print profile_1

clock = Clock(profile_1)
clock.get_all_locations()