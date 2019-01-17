import re
import apodlink
import requests

def randapod():
    url = apodlink.random()
    page = requests.get(url)

    title_raw = re.search("\<title\>.*\<\/title\>", str(page.content)).group(0)
    title = title_raw.partition(">")[2].partition("\\")[0]

    img_raw = re.search("image/.*\"\>", str(page.content)).group(0)
    img = apodlink.base_url + img_raw.partition("\"")[0]

    return title + '\n' + img

#print(randapod())
