import re
import os
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag
import html5lib

# -----------------------------------------------------------------------------
# Scrape Old English poems from the corpus made available 
# by Murray McGillivray from the University of Calgary English department
# -----------------------------------------------------------------------------

def clean_poetic_token(poetic_token):
	poetic_token = str.lower(poetic_token)
	# remove anything not in the OE character set
	poetic_token = re.sub('\n', ' ', poetic_token)
	poetic_token = re.sub('[^0-9a-zþæð.,;:! ]', '', poetic_token)
	poetic_token = re.sub(' +', ' ', poetic_token) 
	return(poetic_token)

def clean_poetic_stanza(poetic_stanza):
	poetic_stanza = str.lower(poetic_stanza)
	poetic_stanza = re.sub('[^0-9a-zþæð.,;:! \n]', '', poetic_stanza)
	poetic_stanza = re.sub(' +', ' ', poetic_stanza) 
	# remove \xa0
	poetic_stanza = re.sub('\xa0', '', poetic_stanza) 
	# remove extra spaces
	poetic_stanza = re.sub(' +', ' ', poetic_stanza) 
	return(poetic_stanza)

def clean_poem_title(poem_title):
	poem_title = str.lower(poem_title)
	poem_title = re.sub(' ','_',poem_title)
	poem_title = re.sub('[^0-9a-zþæð\_]', '', poem_title)
	return(poem_title)


# local directory to deposit poem files
local_corpus_directory = '/Users/ChadMorgan/Documents/old_english/OldEnglishPoetryCorpus/scraped_corpus'

# --- Labyrinth Library hosted poems ----------------------------------------- #
poemdirectory_url = 'http://people.ucalgary.ca/~mmcgilli/OEPoetry/oepoems.htm'
page = requests.get(poemdirectory_url)
soup = BeautifulSoup(page.content, 'html.parser')
poem_links = soup.findAll("a", { "class" : "labyrinth" }, href=True)

for i in range(len(poem_links)):
	# get link to poem page
	poem_ref = poem_links[i]['href']
	poem_page = requests.get(poem_ref)
	poem_soup = BeautifulSoup(poem_page.content, 'html.parser')
	# get link to poem text page
	poem_text_page = requests.get(poem_soup.a.get_text())
	poem_text_soup = BeautifulSoup(poem_text_page.content, 'html.parser')
	# extract dd html tags for the actual poem
	poem_text_raw = poem_text_soup.findAll("dd")
	poem_title = poem_text_soup.findAll('title')[0].get_text()
	poem_title = clean_poem_title(poem_title)
	print(str(i)+": "+poem_title+'\n')
	# clean and concatenate stanzas
	for j in range(len(poem_text_raw)):
		stanza = poem_text_raw[j].get_text()
		stanza = clean_poetic_stanza(stanza)
		if j==0:
			full_poem_text = stanza
		else:
			full_poem_text += stanza
	# create local file and write poem to it
	local_poem_file = local_corpus_directory+'/'+poem_title+'.txt'
	os.system('touch '+local_poem_file)
	f = open(local_poem_file, 'w')
	f.write(full_poem_text)  
	f.close()

# --- OCOEP hosted editions -------------------------------------------------- #

# Note: OCOEP hosten poems are a bit more complicated to parse 
#		due to the notes and word glosses included

def parse_OCOEP_page(poem_main_url,base_url):
	poem_main_page = requests.get(poem_main_url)
	poem_main_soup = BeautifulSoup(poem_main_page.content, "html5lib")
	# get poem src from frame
	frames = poem_main_soup.find_all('frame')
	text_src = frames[0].get('src')
	poem_text_url = base_url + '/' + text_src
	# get raw poem text
	poem_text_page = requests.get(poem_text_url)
	poem_text_soup = BeautifulSoup(poem_text_page.content, "html5lib")
	poem_title = poem_text_soup.findAll('title')[0].get_text()
	poem_title = clean_poem_title(poem_title)
	print(str(i)+": "+poem_title+'\n')
	poem_text_raw = poem_text_soup.findAll(('dd','dt'))
	full_poem_text = ''
	for h in range(len(poem_text_raw)):
		stanza = poem_text_raw[h].contents	
		if poem_text_raw[h].name=='dt':		
			if len(stanza)==0:
				continue
			elif stanza[0].name=='em':
				token = '\n'
				full_poem_text += token
			else:
				continue
		else:
			for j in range(len(stanza)):
				if isinstance(stanza[j], NavigableString):
					token = stanza[j]
					if token=='\n':
						token=' '
					else:
						token = clean_poetic_token(token)
					full_poem_text += token
				else:
					if stanza[j].name=="br":
						token = "\n"
						full_poem_text += token 
					elif stanza[j].name=="p":
						continue
					else:
						token = stanza[j].get_text()
						token = clean_poetic_token(token)
						full_poem_text += token
	full_poem_text = re.sub(' +', ' ', full_poem_text) 
	full_poem_text = re.sub('^\n','', full_poem_text) 
	full_poem_text = re.sub('\n+','\n', full_poem_text) 
	return(poem_title,full_poem_text)



# --- complete hosted editions --- #
base_url = 'http://people.ucalgary.ca/~mmcgilli/OEPoetry'
hosted_poem_links = soup.findAll("a", { "class" : ("done") }, href=True)

for i in range(len(hosted_poem_links)):
	# skipped poems
	if i == 5:
		continue
	# poem main page
	poem_main_url = base_url + "/" + hosted_poem_links[i]['href'].split("/")[-1]
	poem_title,full_poem_text=parse_OCOEP_page(poem_main_url,base_url)
	# create local file and write poem to it
	local_poem_file = local_corpus_directory+'/'+poem_title+'.txt'
	os.system('touch '+local_poem_file)
	f = open(local_poem_file, 'w')
	f.write(full_poem_text)  
	f.close()

# --- in progress editions --- #
base_url = 'http://people.ucalgary.ca/~mmcgilli/ASPR'
inprogress_poem_links = soup.findAll("a", { "class" : ("here") }, href=True)

for i in range(len(inprogress_poem_links)):
	# poem main page
	poem_main_url = base_url + "/" + inprogress_poem_links[i]['href'].split("/")[-1]
	poem_title,full_poem_text = parse_OCOEP_page(poem_main_url,base_url)
	# create local file and write poem to it
	local_poem_file = local_corpus_directory+'/'+poem_title+'.txt'
	os.system('touch '+local_poem_file)
	f = open(local_poem_file, 'w')
	f.write(full_poem_text)  
	f.close()
	


