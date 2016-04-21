"""
Script to calculate the average ratings for all users, all resturants, value of u (average rating for all users for all resturants) from training data
"""

from collections import defaultdict
import json

# Average rating for all users.
def users_avg_ratings(review_file):
	users_avg = defaultdict(float)
	users_review_counts = defaultdict(int)
	with open(review_file, 'r') as f:
		for line in f:
			review = json.loads(line)
			users_avg[review['user_id']] += float(review['stars'])
			users_review_counts[review['user_id']] += 1
		user_avg_file = open('preprocess/user_avg_ratings_train.csv', 'w')
		user_avg_file.write("user_id,avg_ratings,counts\n")
		for user, stars in users_avg.items():
			# users_avg[user] /= users_review_counts[user]
			user_avg_file.write("%s,%s,%s\n" %(user, round(stars / users_review_counts[user], 2), users_review_counts[user]))
		user_avg_file.close()

# Average ratings for all resturants
def restaurants_avg_ratings(review_file):
	rest_avg = defaultdict(float)
	rest_review_counts = defaultdict(int)
	with open(review_file, 'r') as f:
		for line in f:
			review = json.loads(line)
			rest_avg[review['business_id']] += float(review['stars'])
			rest_review_counts[review['business_id']] += 1
		rest_avg_file = open('preprocess/restaurants_avg_ratings_train.csv', 'w')
		rest_avg_file.write('business_id,avg_ratings,counts\n')
		for rest, stars in rest_avg.items():
			rest_avg_file.write("%s,%s,%s\n" % (rest, round(stars / rest_review_counts[rest], 2), rest_review_counts[rest]))
		rest_avg_file.close()

# Average rating for all users for all resturants
def calculate_mu(review_file):
	res = 0.0
	count = 0
	with open(review_file, 'r') as f:
		for line in f:
			review = json.loads(line)
			res += float(review['stars'])
			count += 1
		print res, count, res / count
		with open('preprocess/mu_train.csv', 'w') as output:
			output.write("total_stars,review_counts,avg_stars\n")
			output.write("%s,%s,%s\n" %(res, count, res / count))
			
if __name__ == '__main__':
	# dataset_path = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/"
	users_avg_ratings('preprocess/restaurant_reviews_train.json')
	restaurants_avg_ratings('preprocess/restaurant_reviews_train.json')
	# calculate_mu('preprocess/restaurant_reviews_train.json')