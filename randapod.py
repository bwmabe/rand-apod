#!/usr/bin/env python3

import requests
import math
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime, timezone


def random_url():
    # The first date that picture were posted to APOD continuously
    # June 20th, 1995
    first_date = 803620800
    now = math.floor(datetime.now()
                     .replace(tzinfo=timezone.utc)
                     .timestamp())
    url = 'https://apod.nasa.gov/apod/ap{}.html'
    return url.format(datetime
                      .fromtimestamp(randint(first_date, now))
                      .strftime("%y%m%d"))


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
