#!/usr/bin/env python

"""
Divide the reviews into training and validation 
"""

import os
import json
from sets import Set
import numpy as np
import random

# Divide the datasert into training and validation in 75 - 25 % ratio
def sample(input_filename, trn_filename, val_filename, nlines):

	if os.path.isfile(trn_filename) or os.path.isfile(val_filename):
		print "WARNING: Training and/or validation dataset files exist. Not sampling!"
		return

	f = open(input_filename, "r")

	otrn = open(trn_filename, "w")
	oval = open(val_filename, "w")

	# choice = np.random.choice([range(1,11)], size=(nlines,))
	i = 0
	for l in f.readlines():
		choice = random.choice(range(1, 101))
		if choice < 76:
			otrn.write(l)
		else:
			oval.write(l)
		i += 1


def get_users_businesses(val_filename):

	f = open(val_filename, 'r')

	user_ratings = {}
	for l in f.readlines():
		j = json.loads(l)
		if j["user_id"] not in user_ratings:
			user_ratings[j["user_id"]] = [(j["business_id"], j["stars"])]
		else:
			user_ratings[j["user_id"]].append((j["business_id"], j["stars"]))

	return user_ratings

def main():


	input_filename = "../data/yelp_academic_dataset_review.json"
	trn_filename = "../data/yelp_academic_dataset_review_train.json"
	val_filename = "../data/yelp_academic_dataset_review_validation.json"

	#input_filename = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/restaurant_reviews.json"
	#trn_filname = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review_train.json"
	#val_filename = "/Users/keleigong/Downloads/yelp_dataset_challenge_academic_dataset/yelp_academic_dataset_review_validation.json"


	# Number of lines in the input data file
	# Pre-determined to make things fast, using "wc -l data/yelp_academic_dataset_review.json"
	nlines = 2225213
	#nlines = 1599141


	

	## Sample the input data set into training and validation sets
	sample(input_filename, trn_filename, val_filename, nlines)

	'''
	## Check here if there's enough intersection between training and validation sets
	val_users = get_users_businesses(val_filename)
	trn_users = get_users_businesses(trn_filename)

	val_10_users = Set()
	trn_10_users = Set()
	for u in val_users:
		if len(val_users[u]) >= 40:
			val_10_users.add(u)

	for u in trn_users:
		if len(trn_users[u]) >= 0:
			trn_10_users.add(u)

	print trn_10_users.intersection	(val_10_users)
	'''


if __name__ == "__main__":
	main()
