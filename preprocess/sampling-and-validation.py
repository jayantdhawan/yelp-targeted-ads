#!/usr/bin/env python

import os
import numpy as np


def sample(input_filename, trn_filname, val_filename, nlines):
	f = open(input_filename, "r")

	if os.path.isfile(trn_filname) or os.path.isfile(val_filename):
		print "WARNING: Training and/or validation dataset files exist. Not sampling!"
		return

	otrn = open(trn_filname, "w")
	oval = open(val_filename, "w")

	choices = np.random.choice([0, 1], size=(nlines,))

	i = 0
	for l in f.readlines():
		if choices[i] == 1:
			otrn.write(l)
		else:
			oval.write(l)
		i += 1


def get_top_X(val_filename):

	return None


def main():

	input_filename = "../data/yelp_academic_dataset_review.json"
	trn_filname = "../data/yelp_academic_dataset_review_train.json"
	val_filename = "../data/yelp_academic_dataset_review_validation.json"

	# Number of lines in the input data file
	# Pre-determined to make things fast, using "wc -l data/yelp_academic_dataset_review.json"
	nlines = 2225213




	## Step 1: Sample the input data set into training and validation sets
	sample(input_filename, trn_filname, val_filename, nlines)

	## Step 2: From the validation dataset, generate a list of top X restaurants rated by each of the users
	get_top_X(val_filename)





if __name__ == "__main__":
	main()
