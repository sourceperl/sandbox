from os.path import abspath, dirname, join
import json
from urllib.request import Request, urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup


# some const
main_url = 'https://www.grtgaz.com/medias/actualites'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0'}

# data file
script_dir = (dirname(abspath(__file__)))
data_file = join(script_dir, 'data/articles.json')


def raw_request(url: str) -> bytes:
    uo_req = urlopen(Request(url, headers=headers))
    return uo_req.read()


def soup_request(url: str) -> BeautifulSoup:
    return BeautifulSoup(raw_request(url), 'html.parser')


# extract links from main page
article_url_d = {}
for link in soup_request(main_url).find_all('a'):
    try:
        if 'read-link' in link['class']:
            article_url = urljoin(main_url, link['href'])
            article_url_d[article_url] = raw_request(article_url).decode()
    except KeyError:
        pass

# store result
json.dump(article_url_d, open(data_file, 'w'))
