import json
from collections import Counter

def read_business(file):
	categories = Counter()
	res = open('categories.txt', 'w')
	with open(file, 'r') as f:
		for line in f:
			business = json.loads(line)
			categories.update(business['categories'])
		for category in categories.most_common():
			res.write('%s\t%s\n' % (category[1], category[0]))
		# print categories.most_common(10)
		res.close()

# business = read_business('restaurants.json')

def read_categories(file):
	# categories = []
	with open(file, 'r') as f:
		return f.read().strip().split('\n')

def read_restaurants(file, categories):
	restaurants = dict()
	restaurants_file = open('preprocess/restaurants.json', 'w')
	with open(file, 'r') as f:
		for line in f:
			# json_line = f.readline()
			json_line = json.loads(line)
			if "Yelp Events" not in json_line['categories'] and any(category in json_line['categories'] for category in categories) and json_line['review_count'] > 0:
				restaurants[json_line['business_id']] = json_line
				restaurants_file.write(line)
			# print(json_line)
			# if int(json_line['review_count']) > 50:
				# restaurants[json_line['business_id']] = json_line
		restaurants_file.close()
	# print restaurants
	print(len(restaurants.keys()))
	return restaurants


def read_reviews(file, restaurants):
	global dataset_path
	with open(file, 'r') as f:
		# restaurant_reviews = []
		# line = f.readline()
		# json_line = json.loads(line)
		# print(json_line['business_id'])
		restaurant_reviews = open('preprocess/restaurant_reviews_validation.json', 'w')
		count = 0
		for line in f:
			review = json.loads(line)
			if review['business_id'] in restaurants:
				# restaurant_reviews.append(review)
				user_id = review['user_id']
				business_id = review['business_id']
				stars = review['stars']
				new_line = json.dumps({'user_id': user_id, 'business_id': business_id, 'stars': stars})
				restaurant_reviews.write(new_line + '\n')
				count += 1
			if count % 10000 == 0:
				print(count)
		print count
		# print(len(restaurant_reviews))

if __name__ == '__main__':
	dataset_path = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/"
	file = dataset_path + 'yelp_academic_dataset_business.json'
	categories = read_categories('preprocess/categories-filtered.txt')
	print(len(categories))
	restaurants = read_restaurants(file, categories)
	read_reviews(dataset_path + 'yelp_academic_dataset_review_validation.json', restaurants)

