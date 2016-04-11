import json
import csv

def load_u():
	with open("preprocess/mu.csv", 'rb') as csvfile:
		u_value_file = csv.reader(csvfile, delimiter=',')
		u_value_file.next()
		for row in u_value_file:
			return float(row[2])
	return None

def load_user_rating():
	with open("preprocess/user_avg_ratings.csv", 'rb') as csvfile:
		user_rating_file = csv.reader(csvfile, delimiter=',')
		user_rating_file.next()
		user_rating = {}
		for row in user_rating_file:
			user_rating[row[0]] = (float(row[1]), int(row[2]))
		return user_rating
	return None

def load_business_rating():
	with open("preprocess/restaurants_avg_ratings.csv", 'rb') as csvfile:
		business_rating_file = csv.reader(csvfile, delimiter=',')
		business_rating_file.next()
		business_rating = {}
		for row in business_rating_file:
			business_rating[row[0]] = (float(row[1]), int(row[2]))
		return business_rating
	return None

def load_user_to_business_mapping():
	with open("preprocess/user_to_restaurants_updated.json", 'r') as user_to_business_file:
		user_to_business = {}
		for line in user_to_business_file:
			json_object = json.loads(line)
			user_to_business[json_object['user_id']] = json_object['business'].items()
		return user_to_business
	return None

def load_business_to_user_mapping():
	with open("preprocess/restaurants_to_user_updated.json", 'r') as business_to_user_file:
		business_to_user = {}
		for line in business_to_user_file:
			json_object = json.loads(line)
			business_to_user[json_object['business_id']] = json_object['user_id'].items()
		return business_to_user
	return None


u_ = load_u() 
user_rating = load_user_rating()
business_rating = load_business_rating()
user_to_business = load_user_to_business_mapping()
business_to_user = load_business_to_user_mapping()
