import json
from collections import defaultdict

def user_to_restaurants(review_file):
	mapping = defaultdict(dict)
	with open(review_file, 'r') as f:
		for line in f:
			review = json.loads(line)
			user_id = str(review['user_id'])
			business_id = str(review['business_id'])
			if isinstance(review['stars'], int):
				mapping[user_id][business_id] = review['stars']
		with open('user_to_restaurants.json', 'w') as output:
			# json.dump(mapping, output)
			for user_id, value in mapping.items():
				line = {'user_id': user_id, 'business': mapping[user_id]}
				output.write(str(line) + '\n')


def restaurants_to_user(review_file):
	mapping = defaultdict(dict)
	with open(review_file, 'r') as f:
		for line in f:
			review = json.loads(line)
			user_id = str(review['user_id'])
			business_id = str(review['business_id'])
			if isinstance(review['stars'], int):
				mapping[business_id][user_id] = review['stars']
			# mapping[business_id][]
		with open('restaurants_to_user.json', 'w') as output:
			# json.dump(mapping, output)
			for business_id, value in mapping.items():
				line = {'business_id': business_id, 'user_id': mapping[business_id]}
				output.write(str(line) + '\n')

def category_to_business(restaurant_file, categories_file, output):
	with open(categories_file, 'r') as f:
		categories = f.read().strip().split('\n')
	categories = set(categories)
	mapping = defaultdict(list)
	with open(restaurant_file, 'r') as f:
		for line in f:
			json_object = json.loads(line)
			for category in json_object['categories']:
				mapping[str(category)].append(str(json_object['business_id']))
	with open(output, 'w') as f:
		for category, business_ids in mapping.items():
			if category in categories:
				line = json.dumps({'category': category, 'business_id': business_ids})
				f.write(line + '\n')


if __name__ == "__main__":
	dataset_path = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/"
	# user_to_restaurants(dataset_path + 'restaurant_reviews.json')
	# restaurants_to_user(dataset_path + 'restaurant_reviews.json')
	category_to_business('restaurants.json', 'preprocess/categories-filtered.txt', 'category_to_business.json')