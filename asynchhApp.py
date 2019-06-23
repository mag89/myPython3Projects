#!/usr/bin/env python3.7

from urllib import request as req
from urllib.parse import quote
import re
import time
import asyncio
import aiohttp
from sys import argv


# syncronous generate set of pages with urls on vacancies
def gen_set_of_pages_with_urls(url: str) -> frozenset:
    try:
        response = req.urlopen(url).read()
        data = response.decode("utf-8")
    except:
        data = False
    if data:
        num_of_pages = re.findall(r"data-page=\"\d+\"", data)
        if num_of_pages == []:
            num_of_pages = 0
        else:
            num_of_pages = int(num_of_pages[-2][11:-1])
    else:
        print("Can`t open url for calculate pages, returning 19")
        num_of_pages = 19
    set_of_urls_pages = {(url[0:-1] + str(x)) for x in range(num_of_pages + 1)}
    return frozenset(set_of_urls_pages)


# fetch urls on vacancies and update set of urls on vacancies
async def fetch_urls_on_vac(url: str, session: aiohttp.client.ClientSession) -> None:
    try:
        async with session.get(url) as response:
            data = await response.text()
            urls_on_vac = re.findall(f"https://hh\.ru/vacancy/\d+\?query={search.replace('+', '%20')}", data)
            set_of_urls_on_vac.update(urls_on_vac)
    except:
        print(f"Can`t open page with vacancies - {url}.")


# generete set of urls on vacancies
async def gen_set_of_urls_on_vac(url: str) -> None:
    tasks = []
    set_of_pages_with_urls = gen_set_of_pages_with_urls(url)
    async with aiohttp.ClientSession() as session:
        ##  tasks = [asyncio.create_task(fetch_urls_on_vac(x, session) for x in set_of_pages_with_urls)]
        for _ in set_of_pages_with_urls:
            task = asyncio.create_task(fetch_urls_on_vac(_, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


# fetch tags in vacancy desc
async def fetch_tags_in_vac(url: str, session: aiohttp.client.ClientSession) -> None:
    try:
        async with session.get(url) as response:
            data = await response.text()
            vac_tags = re.findall('data-tag-id="[а-яА-Яa-zA-Z\+-/ ]+"', data)
            all_tags.extend(vac_tags)
    except:
        print(f"Can`t open vacancy - {url}.")


async def get_all_tags() -> None:
    tasks = []
    async with aiohttp.ClientSession() as session:
        for _ in set_of_urls_on_vac:
            task = asyncio.create_task(fetch_tags_in_vac(_, session))
            tasks.append(task)
        await asyncio.gather(*tasks)


# lets sorting tags
def get_sorted_tags() -> list:
    uniq_tags = tuple(frozenset(all_tags))
    dict_of_tags = dict()
    list_of_tags = list()
    for _ in uniq_tags:
        dict_of_tags[_] = all_tags.count(_)
    return sorted(dict_of_tags.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    args = argv[1:3]
    print(args)
    search = quote(args[0])
    print(f"Search vacancies: {search}")
    url = f"https://hh.ru/search/vacancy?area=0&clusters=true&enable_snippets=true&search_field=name&items_on_page=100&text={search}&page=0"
    set_of_urls_on_vac =  set()
    all_tags = list()
    start = time.perf_counter()
    asyncio.run(gen_set_of_urls_on_vac(url))
    asyncio.run(get_all_tags())
    elapsed = time.perf_counter() - start
    count_all_tags = get_sorted_tags()
    print(f"get_all_tags() complit in {elapsed:0.2f} seconds.")
    print(f"Number of vacancies: {len(set_of_urls_on_vac)}")
    if len(count_all_tags) > 0:
        if int(args[1]) > len(count_all_tags):
            num = len(count_all_tags)
            print(f"Found just {num} tags")
        else:
            num = int(args[1])
        i = 1
        for _ in range(num):
            print(f"{i}. {count_all_tags[_][0][12:]} - {count_all_tags[_][1]}")
            i += 1
    else:
        print("Don't found any tags in vacancies")

