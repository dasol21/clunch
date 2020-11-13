from pymongo import MongoClient
from selenium import webdriver
from bs4 import BeautifulSoup
import time

driver = webdriver.Chrome('/Users/dasol/Desktop/Sparta/chromedriver')
driver.implicitly_wait(3)

client = MongoClient('localhost', 27017)
db = client.seoul_matjip

matjips = list(db.restaurants.find({}))[:5]

for matjip in matjips:
    original = matjip['title']
    name = matjip['title'].replace('<b>','').replace('</b>','')
    print(name)

    driver.get('https://map.naver.com/v5/search/'+name)
    time.sleep(3)

    driver.find_element_by_xpath("//span[text()='%s']"%name).click()
    time.sleep(3)


    driver.find_element_by_xpath("//span[text()='사진']").click()
    time.sleep(3)

    driver.find_element_by_xpath("//a[text()='음식']").click()
    time.sleep(3)

    break

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    img = soup.select_one('img[width="87"][height="87"]')

    if img is None:
        continue

    img_url = img['src']

    if img_url is None:
        continue

    db.restaurants.update_one({'title': original}, {'$set': {'img_url': img_url}})