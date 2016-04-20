"""
This module is to load data from pre-processed file in various Data Structure to be used in the algorithm 
"""

import json
import csv
import thread
from collections import defaultdict

category_to_business = {}
business_info = defaultdict(dict)

# Function to load the u (average rating by all users for all rasturants)
def load_u():
	with open("preprocess/mu_train.csv", 'rb') as csvfile:
		u_value_file = csv.reader(csvfile, delimiter=',')
		u_value_file.next()
		for row in u_value_file:
			return float(row[2])
	return None

# Average ratings by all users
def load_user_rating():
	with open("preprocess/user_avg_ratings_train.csv", 'rb') as csvfile:
		user_rating_file = csv.reader(csvfile, delimiter=',')
		user_rating_file.next()
		user_rating = {}
		for row in user_rating_file:
			user_rating[row[0]] = (float(row[1]), int(row[2]))
		return user_rating
	return None

# Average ratings to all resturants
def load_business_rating():
	with open("preprocess/restaurants_avg_ratings_train.csv", 'rb') as csvfile:
		business_rating_file = csv.reader(csvfile, delimiter=',')
		business_rating_file.next()
		business_rating = {}
		for row in business_rating_file:
			business_rating[row[0]] = (float(row[1]), int(row[2]))
		return business_rating
	return None

# Mapping from User to list of tuples where each tuple represent the business Id, Rating given by the user.
def load_user_to_business_mapping(file_name):
	user_to_business = {}
	with open(file_name, 'r') as user_to_business_file:
		for line in user_to_business_file:
			json_object = json.loads(line)
			user_to_business[json_object['user_id']] = json_object['business'].items()
		return user_to_business
	return None

# Mapping from Business to list of tuples where each tuple represent the User Id, Rating given to the resturant.
def load_business_to_user_mapping(file_name):
	business_to_user = {}
	with open(file_name, 'r') as business_to_user_file:
		for line in business_to_user_file:
			json_object = json.loads(line)
			business_to_user[json_object['business_id']] = json_object['user_id'].items()
		return business_to_user
	return None

# Mapping from Business Id to other information about the business
def load_business_info():
	global business_info
	with open("preprocess/restaurants.json", 'r') as f:
		for line in f:
			json_object = json.loads(line)
			full_address = json_object['full_address']
			business_info[json_object['business_id']] = {'categories': json_object['categories'], \
									   'full_address': full_address.replace("\n"," "),
									   'latitude': json_object['latitude'],
									   'longitude': json_object['longitude'],
									   'name': json_object['name']}
	return None

# Mapping from category to list of Business Id belongs to that category
def load_category_to_business_mapping():
	global category_to_business
	with open("preprocess/category_to_business.json", 'r') as f:
		for line in f:
			json_object = json.loads(line)
			category_to_business[json_object['category']] = json_object['business_id']
		return category_to_business
	return None

business_to_user_train = load_business_to_user_mapping("preprocess/restaurants_to_user_train.json")
user_to_business_train = load_user_to_business_mapping("preprocess/user_to_restaurants_train.json")
business_to_user_validation = load_business_to_user_mapping("preprocess/restaurants_to_user_validation.json")
user_to_business_validation = load_user_to_business_mapping("preprocess/user_to_restaurants_validation.json")

load_business_info()
load_category_to_business_mapping()

u_ = round(load_u(), 3) 
user_rating = load_user_rating()
business_rating = load_business_rating()