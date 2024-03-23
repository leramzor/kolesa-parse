import requests
import pandas as pd
from bs4 import BeautifulSoup
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import time
from time import sleep
from random import randint
from selenium.webdriver.firefox.options import Options as FirefoxOptions

data = []
for page in range(1, 2):
    url = "https://kolesa.kz/cars"
    driver = webdriver.Chrome()

    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    cars_section = soup.find("div", class_="a-list")

    cars = cars_section.find_all("div", class_="a-list__item")
    sleep(randint(1,20))
    for car in cars:
        link = car.find("a", class_="a-card__link")
        sleep(randint(1,20))
        driver.get('https://kolesa.kz'+link['href'])
        htmls = driver.page_source
        soups = BeautifulSoup(htmls, "html.parser")
        sleep(randint(1,20))
        WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.CLASS_NAME, "offer")))
        link_car='https://kolesa.kz'+link['href']
        name = soups.find("h1", class_="offer__title").text
        price=soups.find("div", class_="offer__price").text
        phone=soups.find("ul", class_="seller-phones__phones-list")
        comparison = ""
        highlight_span = soups.find("span", class_="summary__highlight")
        if highlight_span is not None:
            if "summary__highlight--red" in highlight_span.get("class"):
                comparison = "дороже"
            elif "summary__highlight--green" in highlight_span.get("class"):
                comparison = "дешевле"

        element = soups.find("div", class_="summary average-price__summary")
        price_text = element.text
        price_compare = re.findall(r'\d+', price_text)

        
        data.append([link_car,name,price,phone,comparison,price_compare])
    driver.back()
    sleep(randint(1,20))

df = pd.DataFrame(data, columns=["Ссылка","Название","Цена","Телефон","Сравнение","Разница в цене"])
writer = pd.ExcelWriter("C:/Users/ernur/Documents/work/cars.xlsx", engine="openpyxl")
df.to_excel(writer, index=False)
writer.close()
