import sys

class Clock():
	def __init__(self, family):
		self.family = family

	# returns a map of user -> location data 
	def get_all_locations(self):
		return {u.name: u.get_location() for u in self.users}


def load_family(user):
	family_members = User.query.filter(User.last_name == user.last_name)
	return Clock(family_members)


# just some bullshit for start up testing 

# profile_1 = open(sys.argv[1]).read()
# print profile_1

# clock = Clock(profile_1)
# clock.get_all_locations()