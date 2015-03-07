# Utility script to parse the dataset provided by Yelp, generating an individual text
# file for each JSON object. Differentiates between User, Review, and Business objects.

# Run in the directory that contains the JSON file(s)

import json, os, re
from pprint import pprint
from pattern.en import suggest

def correct_words(words_list):
	return [tup[0][0] for tup in map(suggest, words_list)]

def lowercase_words(words_list):
	return map(lambda x: x.lower(), words_list)

data = open('../data_sets/yelp_dataset_partial.json')
#data = open('yelp_small.json')
for line in data:
	obj = json.loads(line)
	# user object
	if 'name' in obj and 'user_id' in obj:
		file_name = 'user-' + obj['user_id']
	# review object
	elif 'review_id' in obj:
		file_name = 'review-' + obj['review_id']
		# remove new lines and rewrite text to json object
		new_review = obj['text'].replace('\n\n', ' ').replace('\n', ' ')
		review_words = re.split('\s+', new_review)
		obj['text'] = ' '.join(lowercase_words(review_words))
	# restaurant object
	else:
		file_name = 'restaurant-' + obj['business_id']

	with open(os.path.join('text_files', file_name), 'w') as f:
		json.dump(obj, f)

data.close()