from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import requests


aerolineas = []

options = Options()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get('https://www.airportia.com/airlines/')
print('Recopilando aerolineas...')
time.sleep(5)

page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
driver.close()

filas = soup.select('.textlist-body a')
for f in filas:
    aerolineas.append(f["title"])

data = aerolineas
file1 = open("Lista_Aerolineas.txt","a")
file1.write(str(data))
file1.close()
print(data)
print(len(data))

requests.post('http://127.0.0.1:8000/api/aerolineas', json = data)


