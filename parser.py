import re # реугулярные выражения тут используются не для парсинга html)
import asyncio

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from db import DB


db = DB('sites.db')


def parse_prices(xpath, url):
    driver = webdriver.Chrome()
    driver.get(url)
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, xpath)))
    price_elements = driver.find_elements(By.XPATH, xpath)
    
    prices = []
    # тут удаляются пробелы, как и просили в пдфке тестового, а также меняется запятая на точку
    for element in price_elements:
        cleaned_price = re.sub(r'[^\d.,]', '', element.text)
        cleaned_price = cleaned_price.replace(',', '.')
        
        if cleaned_price:
            prices.append(float(cleaned_price))
    
    return prices
    
    
async def main():
    for title, url, xpath in await db.get_sites_data():
        try:
            prices = parse_prices(xpath, url)
        except Exception:
            print(f'Не получилось спарсить данные с сайта {title}\n')
            continue
        
        print('данные для:', title)
        print('    Найденные цены:', prices)
        print('    Средняя цена:', sum(prices)/len(prices) if prices else 0, '\n')


if __name__ == '__main__':
    asyncio.run(main())