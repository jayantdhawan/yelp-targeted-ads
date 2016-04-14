import json
import csv
import thread
from collections import defaultdict

user_to_business = {}
business_to_user = {}
category_to_business = {}
business_info = defaultdict(dict)
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
	global user_to_business
	with open("preprocess/user_to_restaurants_updated.json", 'r') as user_to_business_file:
		for line in user_to_business_file:
			json_object = json.loads(line)
			user_to_business[json_object['user_id']] = json_object['business'].items()
		return user_to_business
	return None

def load_business_to_user_mapping():
	global business_to_user
	with open("preprocess/restaurants_to_user_updated.json", 'r') as business_to_user_file:
		for line in business_to_user_file:
			json_object = json.loads(line)
			business_to_user[json_object['business_id']] = json_object['user_id'].items()
		return business_to_user
	return None

def load_business_info():
	global business_info
	# business = defaultdict(dict)
	with open("preprocess/restaurants.json", 'r') as f:
		for line in f:
			json_object = json.loads(line)
			full_address = json_object['full_address']
			idx = address.rindex(',')
			address = '_'.join(full_address[0:idx].strip().split())
			zip_code = '_'.join(full_address[idx+1:].strip().split())
			business_info['business_id'] = {'categories': json_object['categories'], \
									   'full_address': (address, zip_code)),
									   'latitude': json_object['latitude'],
									   'longitude': json_object['longitude']}
	return None

def load_category_to_business_mapping():
	global category_to_business
	with open("preprocess/category_to_business.json", 'r') as f:
		for line in f:
			json_object = json.loads(line)
			category_to_business[json_object['category']] = json_object['business_id']
		return category_to_business
	return None

"""
thread.start_new_thread(load_user_to_business_mapping,())
thread.start_new_thread(load_business_to_user_mapping,())
"""
load_business_to_user_mapping()
load_user_to_business_mapping()
load_business_info()
load_category_to_business_mapping()

u_ = load_u() 
user_rating = load_user_rating()
business_rating = load_business_rating()