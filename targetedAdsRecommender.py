"""
This script runs the main algorithm
"""

import loadDataFromFile as data
import locationService as loc
import sys
from sets import Set
from heap import Heap
from math import sqrt

sim_type = 0
store_category_map = {}

# Returns rating of the business given by the user
def get_rating(user_id, business_id):
	all_business = data.user_to_business_train[user_id]
	for (business, rating) in all_business:
		if business == business_id:
			return rating

# Calculate the b_ur as mentioned in the paper (Refer the paper) 
def get_b_ur(user_id, business_id):
	return data.user_rating[user_id][0] + data.business_rating[business_id][0] - data.u_

# Return the list of categories to which the business belongs
def get_category(business_id):
	return data.business_info[business_id]['categories']

# Returns the map with key as category and value as tuple of sum of ratings and number of ratings (Used to find similiarty)
def get_category_map(user, business_list):
	category_map = {}
	for business in business_list:
		rating = get_rating(user, business)
		for category in get_category(business):
			if category not in category_map:
				category_map[category] = (rating, 1)
			else:
				category_map[category] = (rating + category_map[category][0], 1 + category_map[category][1])
	return category_map

# Returns the similarity between two users using the clustering Algorithm
def get_similarity_category(user1, user2):
	global store_category_map
	user1_category = {}
	user2_category = {}

	if user1 not in store_category_map:
		category_map = get_category_map(user1, get_visited_business_for_user(user1))
		store_category_map[user1] = category_map
	user1_category = store_category_map[user1]

	if user2 not in store_category_map:
		category_map = get_category_map(user2, get_visited_business_for_user(user2))
		store_category_map[user2] = category_map
	user2_category = store_category_map[user2]
	
	common_category = list(Set(user1_category.keys()).intersection(Set(user2_category.keys())))
	
	if len(common_category) == 0:
		return 0.0

	similarity = 0.0
	for category in common_category:
		similarity += ((user1_category[category][0] / user1_category[category][1]) - (user2_category[category][0] / user2_category[category][1])) ** 2
	return similarity/(len(common_category) * 25)

# Returns the similiarity between two users without using the clustering Algorithm
def get_similarity_business(user_1, user_2):
	business_for_user_1 = get_visited_business_for_user(user_1)
	business_for_user_2 = get_visited_business_for_user(user_2)
	common_business = list(business_for_user_1.intersection(business_for_user_2))
	if len(common_business) == 0:
		return 0.0
	similarity = 0.0
	for business_id in common_business:
		similarity += (get_rating(user_1, business_id) - get_rating(user_2, business_id)) ** 2
	return similarity/(len(common_business) * 25)

# Calls the Similiarty using clustering or similiarty using non-clustering based on the argument passed to the program
def get_similarity(user_1, user_2):
	if sim_type == 0:
		return get_similarity_business(user_1, user_2)
	else:
		return get_similarity_category(user_1, user_2)

# Returns the predicted rating of a business by a user 
def get_predicted_rating_for_business(user_id, business_id):
	try:
		similar_users = data.business_to_user_train[business_id]
		predicted_rating = 0.0
		
		for (similar_user_id, rating) in similar_users:
			r_ir = rating
			b_ur = get_b_ur(similar_user_id, business_id)
			predicted_rating += ((r_ir - b_ur) * get_similarity(user_id, similar_user_id))
		predicted_rating  = predicted_rating / len(similar_users)
		return predicted_rating + get_b_ur(user_id, business_id)
	except:
		return None

# Returns the top businesses for a given user which he is more likely to visit
def get_top_predicted_list(user_id, business_to_check, number_of_prediction):
	top_business = Heap(number_of_prediction)
	for business_id in business_to_check:
		predicted_rating = get_predicted_rating_for_business(user_id, business_id)
		if predicted_rating:
			top_business.push(round(predicted_rating, 3), business_id)
	return sorted(top_business.get_list(), reverse = True, key = lambda x: x[0])

# Returns the list of businesses thet user have visited
def get_visited_business_for_user(user_id):
	list_tuple = data.user_to_business_train[user_id]
	visited_business = Set([]) 
	for record in list_tuple:
		visited_business.add(record[0])
	return visited_business

# Returns the list of business in nearly location 
def get_nearby_business(location):
	# Return list of business_id
	lat_lng_json = loc.get_latitude_and_longitude_by_location(location)
	business_id_list = loc.get_nearby_business_id(lat_lng_json['lat'], lat_lng_json['lng'], 15)
	return business_id_list

def main():
	global sim_type

	if not (len(sys.argv) == 2 or len(sys.argv) == 5):
		print "python targetedAdsRecommender.py <encrypted_user_id> <Number of Predictions> <location format:530 Brookline Blvd PA 15226)> <Similarity Type 0(Business) | 1(Cluster)>"
		print "For Calculate RMSE: python <Similarity Type 0(Business) | 1(Cluster)>"
		sys.exit()
	
	if len(sys.argv) == 2:
		sim_type = int(sys.argv[1])
		RMSE = 0.0
		count = 0
		for (user, list_business) in data.user_to_business_validation.items():
			for (business, true_rating) in list_business:
				if count%2000 == 0:
					print "count", count
				predicted_rating = get_predicted_rating_for_business(user, business)
				if predicted_rating:
					count += 1
					RMSE += (true_rating - predicted_rating) ** 2
		print "SSE (Sum of Squared Error): ", RMSE
		RMSE = sqrt(RMSE/count)
		print "RMSE: ", RMSE
	else:
		user_id = sys.argv[1]
		number_of_prediction = int(sys.argv[2])
		location = sys.argv[3]
		sim_type = int(sys.argv[4])

		visited_business = get_visited_business_for_user(user_id)
		business_to_check = Set(get_nearby_business(location)) - visited_business
		for business in get_top_predicted_list(user_id, list(business_to_check), number_of_prediction):
			print str(business[0]) + "\t" + data.business_info[business[1]]['name'].ljust(40) + "\t" + data.business_info[business[1]]['full_address']

if __name__ == "__main__":
   main()
