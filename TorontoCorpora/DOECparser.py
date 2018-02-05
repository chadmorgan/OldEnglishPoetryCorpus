import re
import os
from bs4 import BeautifulSoup
from bs4 import NavigableString,Tag
import html5lib

class DOEC_text(object):
    def __init__(self,path): 
        self.path=path
        self.title=''
        self.sentences=[]
        self.split_sentences=[]
        
    def special_char_convert(self,sent):
        char_lookup = {
            '&AE;':'Æ','&D;':'Ð','&T;':'Þ' ,'&ae;':'æ' ,'&amacron;':'a'  
            ,'&amp;':'&' ,'&bbar;':'b','&cmacron;':'c','&d;':'ð' ,'&e;':'e'
            ,'&emacron;':'e','&imacron;':'i','&lbar;':'l','&nmacron;':'n'
            ,'&oe;':'œ','&omacron;':'o'  ,'&pmacron;':'p'  ,'&qmacron;':'q'  
            ,'&rmacron;':'r' ,'&t;':'þ' ,'&tbar;':'þ','&Alpha;':'A','&Eta;':'E'
            ,'&Lambda;':'Λ','&Nu;':'N','&Omega;':'Ω','&Omicron;':'O','&Rho;':'P'
            ,'&Tau;':'T','&omega;':'ω'
        }
        for spec_char in char_lookup.keys():
            sent=re.sub(spec_char,char_lookup[spec_char],sent)
        return sent        
        
    def read_file(self,foreign_words='remove'):
        raw = open(self.path).read()
        soup = BeautifulSoup(raw,'html.parser')
        self.title = soup.find('title',{'type':'st'}).get_text()
        tagged_sentences = soup.findAll('s')
        for s in tagged_sentences:            
            if foreign_words=='remove':
                foreign = s.findAll('foreign')
                for f in foreign:
                    f.extract()
            s = s.get_text().strip()        
            s = self.special_char_convert(s).lower()
            self.sentences.append(s)
        return self
    
    def sentence_splitter(self,punctuation=False):
        for s in self.sentences:
            if punctuation:
                # separate punctuation
                s=re.sub('(?<=\w)([,.&;:?\"!\-\(\)\'])', r' \1', s)
            else:
                s = re.sub('[^a-zæþð ]','',s)
            self.split_sentences.append([s.split(' ')])