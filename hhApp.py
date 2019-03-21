import urllib.request
import re
from datetime import datetime
#import asyncio
#import aiohttp

search = "gamedev"
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
            match_of_desc = re.findall(r"data-tag-id=\"[а-яА-Яa-zA-Z\+-/ ]+\"", page_vacancy)
            match_of_desc = [x[13:-1] for x in match_of_desc]
            if match_of_desc != []:
                list_of_desc.extend(match_of_desc)
        else:
            continue
    return list_of_desc


def get_most_popular_tag(url):
    list_of_desc = get_vacancy_desc(url)
    dictionary_of_vacansys_tag = {}
    for i in list_of_desc:
        dictionary_of_vacansys_tag[i] = list_of_desc.count(i)
    
    for i in dictionary_of_vacansys_tag.items():
        return "{} - {}".format(i[0], i[1])
    

#     for i in dictionary_of_vacansys_teg:
#         if int(dictionary_of_vacansys_teg[i]) >= 100:
#             print("{} - {}".format(i, dictionary_of_vacansys_teg[i]))
        


t0 = datetime.now()
get_most_popular_tag = get_most_popular_tag(url)
t1 = datetime.now()
print("Время выполнения скрипта: ", t1-t0)
print(get_most_popular_tag)

