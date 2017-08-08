import re
import os
import pandas as pd
import gensim
import matplotlib.pyplot as plt


path = '/Users/ChadMorgan/Documents/old_english/OldEnglishPoetryCorpus/scraped_corpus'
contents = os.listdir(path)

corpus_lines = []
word_dict = {}
word_set = set()
line_length_dict = {}
line_length_set = set()

def clean_line(poetry_line):
	poetry_line = re.sub('[.,;:!]','',poetry_line)
	poetry_line = re.sub('\n','',poetry_line)
	poetry_line = re.sub(' $','',poetry_line)
	poetry_line = re.sub('^ ','',poetry_line)
	return(poetry_line)

for poem in contents:
	#	
	poem_lines = []
	with open(path+"/"+poem) as f:
		lines = f.readlines()
	#
	for line in lines:
		if line=='\n':
			continue
		else:
			line = clean_line(line)
			tokenized_line = line.split(' ')
			for token in tokenized_line:
				poem_lines.append(token)
				if token not in word_set:
					word_set.add(token)
					word_dict[token] = 1
				else:
					word_dict[token] += 1
			line_length = len(tokenized_line)
			if line_length not in line_length_set:
				line_length_set.add(line_length)
				line_length_dict[line_length]=1
			else:
				line_length_dict[line_length]+=1
	corpus_lines.append(poem_lines)

# word count
word_count = pd.DataFrame.from_dict(word_dict,orient='index').reset_index()
word_count.columns = ['token','freq']
word_count = word_count.sort_values(by='freq',ascending=False)

word_count_histogram = word_count.groupby('freq').count().reset_index()
word_count_histogram.columns = ['word_freq','bin_count']


# histogram of line lengths
line_length_count = pd.DataFrame.from_dict(line_length_dict,orient='index').reset_index()
line_length_count.columns = ['line_length','freq']
line_length_count = line_length_count.sort_values(by='line_length')
plt.plot(line_length_count['line_length'],line_length_count['freq'])
plt.show()

model = gensim.models.Word2Vec(size=80, window=7, min_count=3,iter=150,sg=1)
model.build_vocab(corpus_lines)
model.train(corpus_lines,total_examples=model.corpus_count,epochs=model.iter)

model.wv.most_similar(positive=['god'])
model.wv.most_similar(positive=['sceal'])
model.wv.most_similar(positive=['eald'])
model.wv.most_similar(positive=['cyning'])
model.wv.most_similar(positive=['æþelingas'])
model.wv.most_similar(positive=['þin'])
model.wv.most_similar(positive=['eorðan'])
model.wv.most_similar(positive=['feorh'])
