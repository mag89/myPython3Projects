import urllib.request
import re
from datetime import datetime

search = "python"
url = "https://hh.ru/search/vacancy?area=0&clusters=true&enable_snippets=true&search_field=name&items_on_page=100&text={}&page=0".format(search)


# блокирующая функция, ждущая ответа от сервера
def load_page(url, timeout=0.1):
    try:
        data = urllib.request.urlopen(url).read()
        page = data.decode("utf-8")
        return page
    except:
        print("Не получилось открыть ссылку: ", url)
        return False


# функция подсчета кол-ва страниц с вакансиями, грузит load_page() 1 раз
def num_of_pages(url):
    t0 = datetime.now()
    page = load_page(url)
    if page:
        num_of_pages = re.findall(r"data-page=\"\d+\"", page)
        if num_of_pages == []:
            num_of_pages = 0
        else:
            num_of_pages = [x[11:-1] for x in num_of_pages][-2]
        t1 = datetime.now()
        print("num_of_pages - ", t1-t0)
        return int(num_of_pages)
    else:
        print("Не открывается ссылка для подчета страниц, возвращаю 19")
        t1 = datetime.now()
        print("num_of_pages - ", t1-t0)
        return 19
    


# функция генерации множества с ссылками страниц с вакансиями (максимум 20 ссылок), грузит load_page() 1 раз
def gen_set_of_urls_pages(url):
    t0 = datetime.now()
    set_of_urls_pages = {(url[0:-1] + str(x)) for x in range(num_of_pages(url) + 1)}
    set_of_urls_pages = frozenset(set_of_urls_pages)
    t1 = datetime.now()
    print("gen_set_of_urls_pages - ", t1-t0)
    return set_of_urls_pages
    


# функция генерации множества с ссылками на сами вакансии (максимум 2000 ссылок), грузит load_page() до 21 раза
def set_of_urls_vacancys(url):
    t0 = datetime.now()
    set_of_urls_vacancys = set()
    for i in gen_set_of_urls_pages(url):
        page = load_page(i)
        if page:
            match_of_urls_vacancys = re.findall(r"https://hh\.ru/vacancy/\d+\?query={}".format(search.replace("+", "%20")), page)
            set_of_urls_vacancys.update(match_of_urls_vacancys)
        else:
            continue
    set_of_urls_vacancys = frozenset(set_of_urls_vacancys)
    t1 = datetime.now()
    print("set_of_urls_vacancys - ", t1-t0)
    print("Кол-во вакансий: ", len(set_of_urls_vacancys))
    return set_of_urls_vacancys



## функция парсинга тегов вакансий (максимум 2000 вакансий), грузит load_page() до 2021 раза
def get_vacancy_desc(url):
    t0 = datetime.now()
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
    t1 = datetime.now()
    print("Общее кол-во тегов вакансий: ", len(list_of_desc))
    print("gen_vacancy_desc - ", t1-t0)
    return list_of_desc
    


# функция подсчета  тегов их сортировка и вывод
def get_most_popular_tag(url):
    list_of_desc = get_vacancy_desc(url)
    dictionary_of_vacansys_tag = {}
    for i in list_of_desc:
        dictionary_of_vacansys_tag[i] = list_of_desc.count(i)
    
    list_of_vacansys_tag = list(dictionary_of_vacansys_tag.items())
    t0 = datetime.now()
    for i in range(len(list_of_vacansys_tag) - 1):
        for z in range(len(list_of_vacansys_tag) - i - 1):
            if list_of_vacansys_tag[z][1] < list_of_vacansys_tag[z+1][1]:
                list_of_vacansys_tag[z], list_of_vacansys_tag[z+1] = list_of_vacansys_tag[z+1], list_of_vacansys_tag[z]
    
    t1 = datetime.now()
    print("Пузырьковая сортировка списка - ", t1-t0)
    return list_of_vacansys_tag
    

t0 = datetime.now()
result = set_of_urls_vacancys(url)
t1 = datetime.now()
print("Время выполнения скрипта: ", t1-t0)
print(result)
