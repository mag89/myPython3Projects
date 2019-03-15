import urllib.request as request
import re
from datetime import datetime

url = "https://hh.ru/search/vacancy?area=0&clusters=true&enable_snippets=true&text=Python&page=0"

def load_page(url):
    data = request.urlopen(url).read()
    page = data.decode("utf-8")
    return page


def num_of_pages(url):
    page = load_page(url)
    num_of_pages = re.findall("data-page=\"\d*\"", page)
    num_of_pages = [x[11:-1] for x in num_of_pages][-2]
    return int(num_of_pages)


def gen_set_of_urls_pages(url):
    set_of_urls_pages = {url[0:-1] + str(x) for x in range(num_of_pages(url) + 1)}
    set_of_urls_pages = frozenset(set_of_urls_pages)
    return set_of_urls_pages


def set_of_urls_vacancys(url):
    set_of_urls_vacancys = set()
    set_of_urls_pages = gen_set_of_urls_pages(url)
    for i in set_of_urls_pages:
        try:
            page = load_page(i)
            match_of_urls_vacancys = re.findall("https://hh.ru/vacancy/\d+\?query=Python", page)
            set_of_urls_vacancys.update(match_of_urls_vacancys)
        except:
            continue
    set_of_urls_vacancys = frozenset(set_of_urls_vacancys)
    return set_of_urls_vacancys


t2 = datetime.now()
print(len(set_of_urls_vacancys(url)))
t3 = datetime.now()
print(t3-t2)