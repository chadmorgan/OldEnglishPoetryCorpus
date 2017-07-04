import requests
from bs4 import BeautifulSoup

def clean_poetic_stanza(poetic_line):
	poetic_line = str.lower(poetic_line)
	# normalize: v -> u, k -> c
	poetic_line = re.sub('v', 'u', poetic_line)
	poetic_line = re.sub('k', 'c', poetic_line)
	# remove anything not in the OE character set
	poetic_line = re.sub('[^a-yþæð\s]', '', poetic_line)
	poetic_line = re.sub(' +', ' ', poetic_line) 
	poetic_line = re.sub('\xa0', '', poetic_line) 
	return(poetic_line)


#poem_url='http://aspr.oepoetry.ca/a32.2.html'
poemdirectory_url = 'http://people.ucalgary.ca/~mmcgilli/OEPoetry/oepoems.htm'

page = requests.get(poemdirectory_url)
soup = BeautifulSoup(page.content, 'html.parser')

print(soup.prettify())

poem_links = soup.findAll("a", { "class" : "labyrinth" }, href=True)

poem_ref = poem_links[0]['href']
poem_page = requests.get(poem_ref)
poem_soup = BeautifulSoup(poem_page.content, 'html.parser')

print(poem_soup.prettify())

poem_text_page = requests.get(poem_soup.a.get_text())
poem_text_soup = BeautifulSoup(poem_text_page.content, 'html.parser')
print(poem_text_soup.prettify())

poem_text_raw = poem_text_soup.findAll("dd")

for stanza in poem_text_raw:
	stanza = stanza.get_text()
	stanza = clean_poetric_line(stanza)
