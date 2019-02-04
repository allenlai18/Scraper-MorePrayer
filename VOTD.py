from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import time
import json

data = {"youversion": {}}

for i in range (1,367):
# for i in range (1,5):

    start_url = "https://www.bible.com/verse-of-the-day"
    ending = "?day=" + str(i)
    full_url = start_url + ending
    print(i)

    driver = webdriver.Firefox()
    # it takes forever to load the page, therefore we are setting a threshold
    driver.set_page_load_timeout(999999)
    try:
        driver.get(full_url)
    except:
        # never ignore exceptions silently in real world code
        with open('john-piper.json', 'w') as outfile:
            json.dump(data, outfile)
        pass

    time.sleep(1.5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    # get image
    slider = soup.find('div', attrs={'class': 'yv-votd-image'})
    divImages = slider.find("div", "placeholder")
    images = divImages.find("img", "large loaded ")
    urlString = "https:" + images.get('src')

    # get the verse
    verseDiv = soup.find('div', 'vertical-center flex-wrap')
    aTag = verseDiv.find('a')
    verse = aTag.contents[0]

    # get content
    divReader = soup.find('div','reader')
    contentElements = divReader.find_all('span','content')
    content = ""
    for element in contentElements:
        content += element.contents[0]

    #write
    day_str = str(i)
    data["youversion"][day_str] = {"votd-image": urlString, "verse": verse, "content": content}

    driver.close()


with open('john-piper.json', 'w') as outfile:
    json.dump(data, outfile)