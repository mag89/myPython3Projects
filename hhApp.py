import urllib.request
import re
from datetime import datetime
#import asyncio
#import aiohttp

search = "python+game"
url = "https://hh.ru/search/vacancy?area=0&clusters=true&enable_snippets=true&search_field=name&items_on_page=100&text={}&page=0".format(search)
# блокирующая функция
def load_page(url, timeout=0.1):
    try:
        data = urllib.request.urlopen(url).read()
        page = data.decode("utf-8")
        return page
    except:
        print("Не получилось открыть ссылку: ", url)
        return False


def num_of_pages(url):
    page = load_page(url)
    if page:
        num_of_pages = re.findall("data-page=\"\d+\"", page)
        if num_of_pages == []:
            num_of_pages = 0
        else:
            num_of_pages = [x[11:-1] for x in num_of_pages][-2]
        return int(num_of_pages)
    else:
        print("Не открывается ссылка для подчета страниц, возвращаю 19")
        return 19


def gen_set_of_urls_pages(url):
    set_of_urls_pages = {(url[0:-1] + str(x)) for x in range(num_of_pages(url) + 1)}
    set_of_urls_pages = frozenset(set_of_urls_pages)
    return set_of_urls_pages


def set_of_urls_vacancys(url):
    set_of_urls_vacancys = set()
    set_of_urls_pages = gen_set_of_urls_pages(url)
    for i in set_of_urls_pages:
        page = load_page(i)
        if page:
            match_of_urls_vacancys = re.findall("https://hh.ru/vacancy/\d+\?query={}".format(search.replace("+", "%20")), page)
            set_of_urls_vacancys.update(match_of_urls_vacancys)
        else:
            continue
    set_of_urls_vacancys = frozenset(set_of_urls_vacancys)
    return set_of_urls_vacancys


t0 = datetime.now()
set_of_urls_vacancys = set_of_urls_vacancys(url)
t1 = datetime.now()
print(t1-t0)
print(len(set_of_urls_vacancys))
print(set_of_urls_vacancys)
