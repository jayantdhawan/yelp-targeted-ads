
def update_user_to_business_file():
	with open("user_to_restaurants.json", 'r') as user_to_business_file:
		write_file = open('user_to_restaurants_updated.json', 'w')
		user_to_business = {}
		for line in user_to_business_file:
			line = line.replace("'", "\"")
			line = line.replace("{u\"", "{\"")
			line = line.replace(", u\"", ", \"")
			line = line.replace(": u\"", ": \"")
			write_file.write(line)
		write_file.close()

def update_business_to_user_file():
	with open("restaurants_to_user.json", 'r') as business_to_user_file:
		write_file = open('restaurants_to_user_updated.json', 'w')
		business_to_user = {}
		for line in business_to_user_file:
			line = line.replace("'", "\"")
			line = line.replace("{u\"", "{\"")
			line = line.replace(", u\"", ", \"")
			line = line.replace(": u\"", ": \"")
			write_file.write(line)
		write_file.close()

update_user_to_business_file()
update_business_to_user_file()