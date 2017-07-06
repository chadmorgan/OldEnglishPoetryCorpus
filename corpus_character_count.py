import re
import os
import pandas as pd

def clean_poetic_line(poetic_line):
	poetic_line = str.lower(poetic_line)
	# normalize: v -> u, k -> c
	poetic_line = re.sub('v', 'u', poetic_line)
	poetic_line = re.sub('k', 'c', poetic_line)
	# remove anything not in the OE character set
	poetic_line = re.sub('[^a-yþæð\s]', '', poetic_line)
	poetic_line = re.sub(' +', ' ', poetic_line) 
	poetic_line = re.sub('\n', '', poetic_line) 
	return(poetic_line)

path = '/Users/ChadMorgan/Documents/old_english/OldEnglishPoetryCorpus/scraped_corpus'
contents = os.listdir(path)

char_set = set()
char_dict = {}
poetry_corpus = []

for poem in contents:
	
	with open(path+"/"+poem) as f:
		lines = f.readlines()
	#
	for line in lines:
		line = clean_poetic_line(line)	
		for c in line:
			if c != " ":
				if c not in char_set:
					char_set.add(c)
					char_dict[c] = 1 
				else:
					char_dict[c] += 1 

char_count = pd.DataFrame.from_dict(char_dict,orient='index').reset_index()
char_count.columns = ['character','freq']
char_count = char_count.sort_values(by='freq',ascending=False)
char_count['pct'] = char_count['freq']/sum(char_count['freq'])

