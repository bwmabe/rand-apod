#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime

#           ja  fe mr  ap  ma  jn  jl  au  sp  oc  no  de
max_days = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
base_url = 'https://apod.nasa.gov/apod/ap{:0>2d}{:0>2d}{:0>2d}.html'

date = datetime.now()

current_year = int(date.strftime("%y"))
current_day = int(date.strftime("%d"))
current_month = int(date.strftime("%m"))


def to_str(data):
    if data < 10:
        return "0" + str(data)
    else:
        return str(data)


def random_url():
    if randint(0, 100) > 25:
        year = randint(0, current_year)
    else:
        year = randint(95, 99)

    if year == current_year:
        month = randint(1, current_month)
    else:
        month = randint(1, 12)

    if month == current_month:
        day = randint(1, current_day)
    else:
        if month != 2:
            day = randint(1, max_days[month - 1])
        else:
            if (year % 4) == 0:
                day = randint(1, 29)
            else:
                day = randint(1, 28)

    return base_url.format(year, month, day)


def get_page(url):
    try:
        page = requests.get(url)
        if page.status_code != requests.codes.ok:
            page.raise_for_status()
        return page.content
    except requests.exceptions.HTTPError as e:
        print(e)
        exit(1)
    except KeyboardInterrupt:
        print("User interrupt")
        exit(0)


def process_page(page):
    soup = BeautifulSoup(page, 'html.parser')

    title = soup.title.string

    image = soup.find_all("img")[0]['src']

    return(title, "https://apod.nasa.gov/apod/{}".format(image))


def randapod():
    page = BeautifulSoup(get_page(random_url()), 'html.parser')
    title = page.title.string
    image = page.find_all("img")[0]['src']
    return(title, "https://apod.nasa.gov/apod/{}".format(image))


if __name__ == '__main__':
    r = randapod()
    print("Title: %s \nURL: %s" % r)
