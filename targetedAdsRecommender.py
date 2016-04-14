import loadDataFromFile as data
import locationService as loc
import sys
from sets import Set
from heap import Heap

def get_rating(user_id, business_id):
	all_business = data.user_to_business[user_id]
	for (business, rating) in all_business:
		if business == business_id:
			return rating

def get_b_ur(user_id, business_id):
	return data.user_rating[user_id][0] + data.business_rating[business_id][0] - data.u_

def get_category(business_id):
	return data.business_info[business_id]['categories']

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

def get_similarity_category(user1, user2):
	user1_category = {}
	user2_category = {}

	user1_category = get_category_map(user1, get_visited_business_for_user(user1))	
	user2_category = get_category_map(user2, get_visited_business_for_user(user2))

	print user2_category
	return 0

def get_similarity(user_1, user_2):
	business_for_user_1 = get_visited_business_for_user(user_1)
	business_for_user_2 = get_visited_business_for_user(user_2)
	common_business = list(business_for_user_1.intersection(business_for_user_2))
	if len(common_business) == 0:
		return 0.0
	similarity = 0.0
	for business_id in common_business:
		similarity += (get_rating(user_1, business_id) - get_rating(user_2, business_id)) ** 2
	return similarity/( len(common_business) * 25)

def get_predicted_rating_for_business(user_id, business_id):
	try:
		similar_users = data.business_to_user[business_id]
		predicted_rating = 0.0
		
		for (similar_user_id, rating) in similar_users:
			r_ir = rating
			b_ur = get_b_ur(similar_user_id, business_id)
			predicted_rating += ((r_ir - b_ur) * get_similarity_category(user_id, similar_user_id))
		predicted_rating  = predicted_rating / len(similar_users)
		return predicted_rating + get_b_ur(user_id, business_id)
	except:
		return None

def get_top_predicted_list(user_id, business_to_check, number_of_prediction):
	top_business = Heap(number_of_prediction)
	for business_id in business_to_check:
		predicted_rating = get_predicted_rating_for_business(user_id, business_id)
		if predicted_rating:
			top_business.push(round(predicted_rating, 3), business_id)
	return top_business

def get_visited_business_for_user(user_id):
	list_tuple = data.user_to_business[user_id]
	visited_business = Set([]) 
	for record in list_tuple:
		visited_business.add(record[0])
	return visited_business

def get_nearby_business(location):
	# Return list of business_id
	lat_lng_json = loc.get_latitude_and_longitude_by_location(location)
	business_id_list = loc.get_nearby_business_id(lat_lng_json['lat'], lat_lng_json['lng'], 5)
	return business_id_list
	# return data.business_rating.keys()

def main():
	if len(sys.argv) != 4:
		print "python targetedAdsRecommender.py <encrypted_user_id> <Number of Predictions> <location format(use underline between words: 530 Brookline Blvd PA 15226)>"
		exit(1)
	user_id = sys.argv[1]
	number_of_prediction = int(sys.argv[2])
	location = sys.argv[3]
	visited_business = get_visited_business_for_user(user_id)
	business_to_check = Set(get_nearby_business(location)) - visited_business
	for business in get_top_predicted_list(user_id, list(business_to_check), number_of_prediction):
		print str(business[0]) + "\t" + data.business_info[business[1]]['name'] + "\t\t\t" + data.business_info[business[1]]['full_address']

if __name__ == "__main__":
   main()
