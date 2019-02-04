# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import unicodedata
import time
import json
from datetime import datetime
from datetime import timedelta

start_date = "2017/01/01"
stop_date = "2017/12/31"

start = datetime.strptime(start_date, "%Y/%m/%d")
stop = datetime.strptime(stop_date, "%Y/%m/%d")


start_url = "https://www.biblegateway.com/devotionals/john-piper-devotional"
devotional_name = "/john-piper-devotional/"
pre_url = start_url + devotional_name
data = {"john-piper-devotional": {}}


date_format = datetime.strftime(start,"%Y/%m/%d")
full_url = pre_url + date_format

driver = webdriver.Firefox()
driver.set_page_load_timeout(5)
try:        
    driver.get(full_url)
except:
    # never ignore exceptions silently in real world code
    with open('JohnPiper.json', 'w') as outfile:
        json.dump(data, outfile)
    pass


soup = BeautifulSoup(driver.page_source, 'html.parser')
# let titleElement = try! doc.select("title").first()
# title = soup.find('title')
# print(title.get_text())
    # let paragraphs: Elements = try! doc.select(".col-xs-12").select("p")

paragraphs = soup.find("div", { "class" : "col-xs-12" })
title = paragraphs.find('h3')
allP = paragraphs.find_all("p")
# print(str(allP[1].text.encode('utf-8')).replace("\\xe2\\x80\\x99","'"))
# print(paragraphs.encode('utf-8'))
# p = str(allP[1].get_text().encode('utf-8')).replace("\\xe2\\x80\\x99","'")
allText = allP[0].get_text()
for p in allP[1:]:
    allText += "\n" + p.get_text()


# print(allText)
driver.close()



