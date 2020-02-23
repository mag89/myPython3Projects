import urllib.request
import re
import sqlite3
from datetime import date as date


# функция загрузки HTML страницы
def load(url):
    try:
        page = urllib.request.urlopen(url, timeout=3).read()
        decoding_page = page.decode("utf-8")
        return decoding_page
    except Exception as e:
        print(e)
        print("Невозможно открыть страницу: {}".format(url))


# функция для поиска совпадений тарифов метро
def grab_tariffs_metro(url):
    load_page = load(url)

    # ищу совпадения имени и цены тарифов с помощью регулярных выражений(помещаются в списки)
    n_match = re.findall("<td\s+class=\"tariffTable__name\">.+</td>", load_page)
    p_match = re.findall("<td\s+class=\"tariffTable__price\">\d+</td>", load_page)

    if p_match != [] or n_match != []:
        # оставляю нужные срезы в списках
        n_match = [x[31:-5] for x in n_match]
        # p_match должен содержать  число количества(поездок/дней) и стоимость
        for i in range(len(p_match)):
            n_123 = ""
            # оставляю только число поездок/дней
            for j in n_match[i]:
                if j in "0123456789":
                    n_123 += j
            p_match[i] = int(n_123), int(p_match[i][32:-5])

        # создаю словарь всех тарифов ключ-имя, значение-стоимость и кол-во поездок.
        # Создаю и заполняю словари по каждой группе тарифов
        tariffs_all = {n: p for n, p in zip(n_match, p_match)}
        tariff_1 = {}
        tariff_2 = {}
        for i in tariffs_all.items():
            if "поезд" in i[0] and "монорельсе" not in i[0]:
                tariff_1[i[0]] = i[1]
            elif "сут" in i[0] or "дней" in i[0]:
                tariff_2[i[0]] = i[1]

        # переписываю общий словарь тарифов по группам тарифов
        tariffs_all = {1: tariff_1, 2: tariff_2}
        return tariffs_all
    else:
        print("Совпаданий на странице {}... не найдено".format(url[0:23]))


# функция для поиска совпадений рабочих и выходных дней календаря
def grab_calendar(url):
    load_page = load(url)

    # ищу совпадения с помощью регулярок
    working_days = re.findall("рабочие дни	&mdash; \d{3}<br.*/>", load_page)
    resting_days = re.findall("выходных/праздничных &mdash; \d{3}</p>", load_page)

    if working_days != [] or resting_days != []:
        # очищаю совпадения от всего лишнего и превращаю в int
        working_days = int(working_days[0][20:-6])
        resting_days = int(resting_days[0][29:-4])

        return working_days, resting_days
    else:
        print("Совпаданий на странице {}... не найдено".format(url[0:23]))


# функция запроса данных у пользоввтеля для расчета
def input_user_data():
    # инициализирую переменные
    vacation_days, work_trips, rest_trips = None, None, None
    # обрабатываю исключения введенных данных
    while not isinstance(vacation_days, int) or vacation_days < 0 or vacation_days > 345:
        try:
            vacation_days = int(input("Сколько(от 0 до 345) календарных дней отпуска в году?: "))
        except ValueError:
            print("\nВнимание! Это должно быть целое число, не более 345 дней.")

    while not isinstance(work_trips, int):
        try:
            work_trips = int(input("\nВведите кол-во поездок в будний день: "))
        except ValueError:
            print("\nВнимание! Это должно быть целое число.")

    while not isinstance(rest_trips, int):
        try:
            rest_trips = int(input("\nВведите среднее количество поездок в выходной день: "))
            print()
        except ValueError:
            print("\nВнимание! Это должно быть целое число.")

    return vacation_days, work_trips, rest_trips


# функция парсинга из прайса для бд
def values_for_db(price):
    values = []
    for i in price.items():
        for j in i[1].items():
            tup = (i[0], j[0], j[1][0], j[1][1])
            values.append(tup)
    return values


# функция создания таблицы если она не существует
def create_price_table():
    conn = sqlite3.connect("metroPrice.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS price_table (price_group INTEGER, price_name TEXT, price_period INTEGER,"
                   "price_cost INTEGER)")


# функция подсчета кол-ва рабочих и выходных дней
def calc_work_and_rest_days(vacation_days, calendar):
    if vacation_days % 7 == 0:
        work_days = calendar[0] - vacation_days // 7 * 5
        rest_days = calendar[1] + vacation_days // 7 * 5
    elif 1 <= vacation_days % 7 <= 5:
        work_days = calendar[0] - (vacation_days // 7 * 5 + vacation_days % 7)
        rest_days = calendar[1] + (vacation_days // 7 * 5 + vacation_days % 7)
    else:
        work_days = calendar[0] - (vacation_days // 7 * 5 + 5)
        rest_days = calendar[1] + (vacation_days // 7 * 5 + 5)
    return work_days, rest_days


# функция расчета выгодного тарифа
def calc():
    # считаю кол-во рабочих и выходных дней пользователя
    vacation_days, work_trips, rest_trips = input_user_data()
    try:
        calendar = grab_calendar("http://www.consultant.ru/law/ref/calendar/"
                                 "proizvodstvennye/{}/".format(date.today().year))
    except TypeError:
        print("\nЗагружаю среднее количество рабочих,выходных дней в году\n")
        calendar = 247, 118

    # считаю количество поездок пользователя
    work_days, rest_days = calc_work_and_rest_days(vacation_days, calendar)
    trips_in_year = work_days*work_trips + rest_days*rest_trips

    # открываю соединение с бд, если бд нет то sqlite3.connect создает ее автоматически
    conn = sqlite3.connect("metroPrice.db")
    cursor = conn.cursor()
    # создаю таблицу если не существует
    create_price_table()
    # селект данных из price_table
    cursor.execute("SELECT * FROM price_table")
    data_in_table = cursor.fetchall()
    try:
        price = grab_tariffs_metro("http://www.mosmetro.ru/tariffs/unity/")
        # обработка данных из прайса для бд
        data_in_price = values_for_db(price)
        # записываем данные если таблица пустая, еcли полная - обновляю если данные отличаются
        if data_in_table == []:
            cursor.executemany("INSERT INTO price_table VALUES (?, ?, ?, ?)", data_in_price)
        else:
            if data_in_table != data_in_price:
                cursor.executemany("UPDATE OR IGNORE price_table SET price_group=?, price_name=?, price_period=?,"
                                   "price_cost=?", data_in_price)
        conn.commit()
    except Exception as e:
        print(e)
        # ссылка недоступна - загружаюсь из бд
        print("\nЗагружаю данные из локальной бд\n")
        price1 = {}
        price2 = {}
        if data_in_table != []:
            for i in data_in_table:
                if i[0] == 1:
                    price1.update({i[1]: (i[2], i[3])})
                elif i[0] == 2:
                    price2.update({i[1]: (i[2], i[3])})
            price = {1: price1, 2: price2}
        else:
            print("В локальной бд нет записей данных, программа запущена впервые.\n повторите позже...\n")
            price = False
    cursor.close()
    conn.close()

    # если price = True то выводи ответ
    if price:
        result_d = dict()
        for i in price[1].items():
            x = round(trips_in_year/i[1][0]*i[1][1])
            print("Стотмость проездного в год по тарифу {} для вас составляет: {} руб".format(i[0], x))
            result_d[x] = i[0]

        for i in price[2].items():
            x = round((calendar[0]+calendar[1])/i[1][0]*i[1][1])
            print("Стотмость проездного в год по тарифу {} для вас составляет: {} руб".format(i[0], x))
            result_d[x] = i[0]

        # вывожу выгодный тариф
        result = sorted(result_d)
        print("\nДля Вас выгоден тариф {} - {} руб/год".format(result_d[result[0]], result[0]))
        print("Для Вас стоимость 1 поездки по "
              "тарифу {} составляет {} руб".format(result_d[result[0]], round(result[0]/trips_in_year, 2)))


calc()
