import re
from bs4 import BeautifulSoup
import requests


def monitor():
    url = requests.get('https://monitordolarvzla.com/category/promedio-del-dolar/')
    soup = BeautifulSoup(url.content, 'html.parser')

    result = soup.find('div', {'class': 'entry-content'})
    rows  = result.find_all('p', limit = 1, recursive = False)
    format_result = rows
    format_result1 = str(format_result)
    matchObj = re.search( r'([+-]?[0-9]+([.][0-9]+([.][0-9]+([,][0-9]+))))', format_result1, re.M|re.I)
    if matchObj:
        f = float(matchObj.group(1))
        print(f)
    else:
        print("No match!!")





if __name__ == '__main__':
    monitor()