import requests
from bs4 import BeautifulSoup

resp = requests.get("http://www.baidu.com")
resp.encoding = "utf-8"
print(resp.text)

soup = BeautifulSoup(resp.text, 'lxml')
tr_list = soup.find('tbody').find_all('tr')
