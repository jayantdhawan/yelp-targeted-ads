import json
from collections import Counter, defaultdict

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

def category_to_business(file, output):
	categories = defaultdict(list)
	with open(file, 'r') as f:
		for line in f:
			json_object = json.loads(line)
			for category in json_object['categories']:
				categories[category].append(json_object['business_id'])
	with open(output, 'w') as f:
		json.dump(categories, f)

if __name__ == '__main__':
	# read_business('restaurants.json')
	category_to_business('restaurants.json', 'category_to_business.json')