from collections import Counter
from os.path import abspath, dirname, join
from string import punctuation
import json
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


# data file
script_dir = (dirname(abspath(__file__)))
data_file = join(script_dir, 'data/articles.json')

# load articles from json file
articles_d = json.load(open(data_file, 'r'))

# extract readable text from all articles
txt = ''
for url, html_content in articles_d.items():
    txt += BeautifulSoup(html_content, 'html.parser').get_text(separator='\n', strip=True)

# tokenize readable text
words_l = word_tokenize(txt, language='french')

# reject some words from words list
reject_l = stopwords.words('french') 
reject_l.extend(punctuation) 
reject_l.extend(['’', '«', '»'])
reject_l.extend(['grtgaz', 'retour', 'chez', 'plus'])
word_l = [word for word in words_l if word.lower() not in reject_l]

# show 10 most common words
for word, count in Counter(word_l).most_common(10):
    print(f'#{count:03d}\t{word}')
