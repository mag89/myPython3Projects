import urllib.request
import re
from datetime import datetime
#import asyncio
#import aiohttp

search = "java+game"
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
        num_of_pages = re.findall(r"data-page=\"\d+\"", page)
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
    for i in gen_set_of_urls_pages(url):
        page = load_page(i)
        if page:
            match_of_urls_vacancys = re.findall(r"https://hh\.ru/vacancy/\d+\?query={}".format(search.replace("+", "%20")), page)
            set_of_urls_vacancys.update(match_of_urls_vacancys)
        else:
            continue
    set_of_urls_vacancys = frozenset(set_of_urls_vacancys)
    return set_of_urls_vacancys


def get_vacancy_desc(url):
    list_of_desc = list()
    for i in set_of_urls_vacancys(url):
        page_vacancy = load_page(i)
        if page_vacancy:
            match_of_desc = re.findall(r"<div.+vacancy-description.+>.+</div>", page_vacancy)
            list_of_desc.append(match_of_desc)
        else:
            continue
    
    list_of_strongs = list()
    for i in list_of_desc:
        match_of_strongs = re.findall(r"^\".+$\"", i[0])
        if match_of_strongs != []:
#             match_of_strongs = [x[4:-5] for x in match_of_strongs]
            list_of_strongs.append(match_of_strongs)
        else:
            print(len(i))
    return list_of_strongs
        


t0 = datetime.now()
list_of_desc = get_vacancy_desc(url)
t1 = datetime.now()
print(t1-t0)
print(len(list_of_desc))
print(list_of_desc)
