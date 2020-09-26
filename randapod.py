#!/usr/bin/env python3

import re
import requests
from random import *
from datetime import *

#           ja  fe mr  ap  ma  jn  jl  au  sp  oc  no  de
max_days = [31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
base_url = 'https://apod.nasa.gov/apod/'

date = datetime.now()

current_year = int(date.strftime("%y"))
current_day = int(date.strftime("%d"))
current_month = int(date.strftime("%m"))

def to_str(data):
    if data < 10:
        return "0" + str(data)
    else:
        return str(data)

def random():
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
                
    return base_url + 'ap' + to_str(year) + to_str(month) + to_str(day) + '.html'

#print(randapod())

def randapod():
    url = random()
    page = requests.get(url)

    title_raw = re.search("\<title\>.*\<\/title\>", str(page.content)).group(0)
    title = title_raw.partition(">")[2].partition("\\")[0]

    img_raw = re.search("image/.*\"\>", str(page.content)).group(0)
    img = base_url + img_raw.partition("\"")[0]

    return title + '\n' + img

if __name__ == '__main__':
    print(randapod())
