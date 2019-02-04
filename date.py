# encoding: utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time
import json
from datetime import datetime
from datetime import timedelta

start_date = "2017/01/01"
stop_date = "2017/01/05"

start = datetime.strptime(start_date, "%Y/%m/%d")
stop = datetime.strptime(stop_date, "%Y/%m/%d")


start_url = "https://www.biblegateway.com/devotionals/john-piper-devotional"
devotional_name = "/john-piper-devotional/"
pre_url = start_url + devotional_name
data = {"john-piper-devotional": {}}

while start <= stop:
    date_format = datetime.strftime(start,"%Y/%m/%d")
    full_url = pre_url + date_format

    driver = webdriver.Firefox()
    # driver.set_page_load_timeout(5)
    try:        
        driver.get(full_url)
    except:
        # never ignore exceptions silently in real world code
        with open('JohnPiper.json', 'w') as outfile:
            json.dump(data, outfile)
        pass

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    paragraphs = soup.find("div", { "class" : "col-xs-12" })
    title_soup = paragraphs.find('h3')
    allP = paragraphs.find_all("p")
    title = title_soup.get_text()
    print(title)
    allText = allP[0].get_text()
    for p in allP[1:]:
        allText += "\n" + p.get_text()
    data["john-piper-devotional"][str(date_format)] = {"title": title, "content": allText}


    driver.close()

    # iterate
    start = start + timedelta(days=1)  # increase day one by one




with open('JohnPiper.json', 'w') as outfile:
    json.dump(data, outfile)