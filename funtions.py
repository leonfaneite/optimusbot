import os
from telegram import *
import qrcode
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update,ReplyKeyboardMarkup,ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext , MessageHandler,  Filters, ConversationHandler
from telegram import ChatAction
from collections import defaultdict
import json
import requests
from bs4 import BeautifulSoup
import re


INPUT_TEXT, INPUT_L , INPUT_M , INPUT_N = range(4)

list_valores=[]


reply_keyboard = [
    ['pesos'],
    ['soles']
]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

Initial_keyboard = [
    ['Genera un Codigo QR'],
    ['Precio del BTC'],['Dolar MonitorVZLA'],
    ['Precio del DolarToday'],
    ['Calcular Giro a VEN'],
    ['Salir']
]
i_markup = ReplyKeyboardMarkup(Initial_keyboard, one_time_keyboard=True)

def inicio( update, context):
    update.message.reply_text(f'''Hola {update.effective_user.first_name} , que puedo hacer por ti hoy? :) 
       
    ''',reply_markup = i_markup )

    return INPUT_L

def closed(update,context):
    
    update.message.reply_text("Fue un placer ayudarte :) ",reply_markup=ReplyKeyboardRemove())
    
    return ConversationHandler.END


#####,######################################################################
#CODIGO DE DOLAR TODAY Y BITCOIN

def dolartoday_total():

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

    #print({:,.2f}'.format(g))
def dolartoday(update,context):
    total = dolartoday_total()
    update.message.reply_text(f'El dolartoday esta en :Bs {"{:,.2f}".format(total)}' ,reply_markup = i_markup )




def btc_scraping(update,context):
    url = requests.get('https://awebanalysis.com/es/coin-details/bitcoin/')
    soup = BeautifulSoup(url.content, 'html.parser')

    result = soup.find('td', {'class': 'wbreak_word align-middle coin_price'})
    format_result = result.text
 
    update.message.reply_text(f'El Bitcoin esta en:  {format_result}',reply_markup = i_markup )


def monitor_dolar():
    url = requests.get('https://monitordolarvzla.com/category/promedio-del-dolar/')
    soup = BeautifulSoup(url.content, 'html.parser')

    result = soup.find('div', {'class': 'entry-content'})
    rows  = result.find_all('p', limit = 1, recursive = False)
    format_result = rows
    format_result1 = str(format_result)
    matchObj = re.search( r'([+-]?[0-9]+([.][0-9]+([.][0-9]+([,][0-9]+))))', format_result1, re.M|re.I)
    if matchObj:
        f = matchObj.group(1)
        raw = f.split(".")
        num = "".join(raw)
        total = float(num.replace(',', '.'))
         
        
    else:
        print("No match!!")

    return total

def monitor(update,context):
    dolar_mon = monitor_dolar()
    update.message.reply_text(f'El dolar  Monitor Dolar esta en:  {"{:,.2f}".format(dolar_mon)}',reply_markup = i_markup )
    


##############################################################################
#FUNCIONES PARA GENERAR QR


def qr_coman(update,context):
    update.message.reply_text("Enviame el codigo QR")
    return INPUT_TEXT

def input_string(update,context):
        
    text = update.message.text
    filename= generate_qr(text)
    chat= update.message.chat
    send_qr(filename,chat)
    update.message.reply_text("que mas deseas hacer?",reply_markup = i_markup)
    return INPUT_L

def generate_qr(txt):
    filename=txt + ".jpg"
    img = qrcode.make(txt)
    img.save(filename)
    return filename

def send_qr(filename,chat):

    chat.send_action(
        action=ChatAction.UPLOAD_PHOTO,
        timeout=None)
    chat.send_photo(
        photo=open(filename,'rb')
    )

    os.unlink(filename)


#####################################################################
#CAMBIOS DE MONEDA


def question(update,context):
    update.message.reply_text("Que deseas enviar?",reply_markup=markup,)
    return INPUT_M



def tipo_envio(update,context):
    text = update.message.text
    if text == "pesos":
        cant_peso(update,context)
    elif text =="soles":
        cant_soles(update,context)


#########################################################################
########Cambio en SOLES
def cant_soles(update,context):

    update.message.reply_text("a que tasa deseas enviar?")
    
    return INPUT_M


def pedir_tasa_soles(update,context):
    
    tasa = update.message.text
    list_valores.append(tasa)
    update.message.reply_text("que monto vas a enviar?")   
    return INPUT_N
    

def total_enviar_soles(update,context):

    for i in list_valores:

        m = float(i)
    
    monto_env = float(update.message.text)
    
    total = monto_env * m
    total_real = float("{0:.2f}".format(total))

    dt = total_real / dolartoday_total()

    
    
    do_moni = total_real / monitor_dolar()

    print(do_moni)


    update.message.reply_text(f'El total a enviar es : Bs {"{:,.2f}".format(total_real)} y podras comprar $ {"{0:.2f}".format(dt)} al cambio de dolartoday y $ {"{0:.2f}".format(do_moni)} al Cambio de MonitorDolarVZLA ' ,reply_markup = i_markup )
    return INPUT_L

##############################################################

def cant_peso(update,context):

    update.message.reply_text("a que tasa deseas enviar?")
    
    return INPUT_M


def pedir_tasa(update,context):
    
    tasa = update.message.text
    list_valores.append(tasa)
    update.message.reply_text("que monto vas a enviar?")   
    return INPUT_N
    

def total_enviar(update,context):

    for i in list_valores:

        m = float(i)
    
    monto_env = float(update.message.text)
    
    total = monto_env / m
    total_real = float("{0:.2f}".format(total))

    dt = total_real / dolartoday_total()

    
    
    do_moni = total_real / monitor_dolar()

    print(do_moni)


    update.message.reply_text(f'El total a enviar es : Bs {"{:,.2f}".format(total_real)} y podras comprar $ {"{0:.2f}".format(dt)} al cambio de dolartoday y $ {"{0:.2f}".format(do_moni)} al Cambio de MonitorDolarVZLA ' ,reply_markup = i_markup )
    return INPUT_L



















    #def probe(update,context):
#    button= InlineKeyboardButton(
#        text="Facebook",
#        url="www.facebook.com"
#
#    )
#
#    button1= InlineKeyboardButton(
#        text="Twitter",
#        url="www.twitter.com"
#
#    )
#
#    update.message.reply_text(
#        text="A donde quieres ir?",
#        reply_markup=InlineKeyboardMarkup([
#            [button],
#            [button1]
#
#        ])
#
#    )