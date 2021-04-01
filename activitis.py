import  telebot
from  telebot import types
from bs4 import BeautifulSoup  #del módulo bs4, necesitamos BeautifulSoup
import requests
import schedule
from collections import defaultdict
from data import *












def btc_scraping():
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')

    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text

    return format_result


def report():
    btc_price = f'El precio de Bitcoin es de {btc_scraping()}'
    bot_send_text(btc_price)

def report_dolar():
    dolar = f'El precio de Dolartoday es de Bs {dolartoday()}'
    bot_send_text(dolar)



def dolartoday():

    results = defaultdict(list)
    r = requests.get("https://s3.amazonaws.com/dolartoday/data.json")
    req = r.json()
    if r.status_code == 200:
         for d in req.values():
             for k,v in d.items(): 
                 a = results[k].append(v)
    
    k = list(results.keys())
    v = list(results.values())
    
    final = dict(results)

    g = final.get('dolartoday','no existe')

    return g[0]


def msm():
    
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('/btc')
    itembtn2 = types.KeyboardButton('/dolar')
    markup.add(itembtn1, itembtn2)
    bot.send_message(chat_id, "Choose one letter:", reply_markup=markup)






