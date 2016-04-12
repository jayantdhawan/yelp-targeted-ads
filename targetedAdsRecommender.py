import loadDataFromFile as data
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

def get_similarity(user_1, user_2):
	business_for_user_1 = get_visited_business_for_user(user_1)
	business_for_user_2 = get_visited_business_for_user(user_2)
	common_business = list(business_for_user_1.intersection(business_for_user_2))
	if len(common_business) == 0:
		return 0.0
	similarity = 0.0
	for business_id in common_business:
		similarity += (get_rating(user_1, business_id) - get_rating(user_2, business_id)) ** 2
	return similarity/len(common_business)

def get_predicted_rating_for_business(user_id, business_id):
	similar_users = data.business_to_user[business_id]
	predicted_rating = get_b_ur(user_id, business_id)
	
	for (similar_user_id, rating) in similar_users:
		r_ir = rating
		b_ur = get_b_ur(similar_user_id, business_id)
		predicted_rating += ((r_ir - b_ur) * get_similarity(user_id, similar_user_id))
	return predicted_rating

def get_top_predicted_list(user_id, business_to_check, number_of_prediction):
	top_business = Heap(number_of_prediction)
	for business_id in business_to_check:
		top_business.push(get_predicted_rating_for_business(user_id, business_id), business_id)
	return top_business

def get_visited_user_for_business(business_id):
	list_tuple = data.business_to_user[business_id]
	set_user = Set([])
	for record in list_tuple:
		set_user.add(record[0])
	return set_user

def get_visited_business_for_user(user_id):
	list_tuple = data.user_to_business[user_id]
	visited_business = Set([]) 
	for record in list_tuple:
		visited_business.add(record[0])
	return visited_business

def main():
	if len(sys.argv) != 3:
		print "python targetedAdsRecommender.py <encrypted_user_id> <Number of Predictions>"
		exit(1)
	user_id = sys.argv[1]
	number_of_prediction = int(sys.argv[2])
	visited_business = get_visited_business_for_user(user_id)
	business_to_check = Set(data.business_rating.keys()) - visited_business
	for business in get_top_predicted_list(user_id, list(business_to_check), number_of_prediction):
		print business

if __name__ == "__main__":
   main()
