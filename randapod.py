#!/usr/bin/env python3
# Randapod: Returns a random NASA APOD URL
# (c) 2019 - 2021 bwmabe

import requests
import math
import sys
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from random import randint
from datetime import datetime, timezone


# Returns a URL to an APOD page from between June 20th 1995 and today
#
# @return the afore mentioned URL
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


# Retrives a page and checks that retrieval was okay
#
# @param a URI that points to an APOD page
# @return the contents of an APOD page
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


# Retrives a page and checks that retrieval was okay, asynchronously
#
# @param a URI that points to an APOD page
# @return the contents of an APOD page
async def get_page_async(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()


# Extracts the <title> and an <img> element.
# On APOD pages; the Picture of the Day is the only <img> element
#
# @return a tuple containing page title and a URI to the image
def randapod():
    page = BeautifulSoup(get_page(random_url()), 'html.parser')
    title = page.title.string
    image = page.find_all("img")[0]['src']
    return(title, "https://apod.nasa.gov/apod/{}".format(image))


# Extracts the <title> and an <img> element, asynchronously
# On APOD pages; the Picture of the Day is the only <img> element
#
# @return a tuple containing page title and a URI to the image
async def randapod_async():
    page = BeautifulSoup(await get_page_async(random_url()), 'html.parser')
    title = page.title.string
    image = page.find_all("img")[0]['src']
    return(title, "https://apod.nasa.gov/apod/{}".format(image))


if __name__ == '__main__':
    if len(sys.argv) >= 1:
        if sys.argv[1] == "async" or sys.argv[1] == "-a":
            r = asyncio.run(randapod_async())
        else:
            print("Unknown argument")
            exit(1)
    else:
        r = randapod()
    print("Title: %s \nURL: %s" % r)
