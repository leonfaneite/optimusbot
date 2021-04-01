import  telebot

from  telebot import types

from data import *

from activitis import *

#from telegram import *

#from telegram.ext import Updater




@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Bienvenido mi nombre es Opimus mis comandos son /btc para consultar Bitcoin, /dolar para consultar el dolartoday, /cambio para hacer conversiones")



@bot.message_handler(commands=['cambio'])
def send_welcome(message):
	bot.reply_to(message, f'Que tipo de cambio quieres hacer? {msm()}')
    


@bot.message_handler(commands=['bitcoin','btc'])
def send_welcome(message):
	bot.reply_to(message,f'El precio de Bitcoin es de {btc_scraping()}')

@bot.message_handler(commands=['dolartoday','dolar'])
def send_welcome(message):
	bot.reply_to(message,f'El precio de Dolartoday es de Bs {dolartoday()}')



@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message,"disculpa no entiendo lo que me quieres decir, usa el comando /help para ver mis funciones" )



if __name__ == "__main__":
    
    bot.polling()
    



