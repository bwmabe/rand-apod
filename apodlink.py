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
        month = randint(1, current_year)
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
