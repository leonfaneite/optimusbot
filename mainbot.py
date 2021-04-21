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
from funtions import *






################################################################################


if __name__ == '__main__':
    mon_dolar=0

    
    updater = Updater('TOKEN', use_context=True)
   
       
####################manejador del QR
    


    dp = updater.dispatcher.add_handler(ConversationHandler(
        entry_points=[CommandHandler('start', inicio)
        ],
        states={

             INPUT_L :[ MessageHandler(Filters.regex('^Precio del DolarToday$'), dolartoday),
                        MessageHandler(Filters.regex('^Precio del BTC$'), btc_scraping),
                        MessageHandler(Filters.regex('^Dolar MonitorVZLA$'), monitor),
                        MessageHandler(Filters.regex('^Genera un Codigo QR$'), qr_coman),
                        MessageHandler(Filters.regex('^Calcular Giro a VEN$'), question),
                        MessageHandler(Filters.regex('^Salir$'), closed)
                        ],
            INPUT_M:[ MessageHandler(Filters.regex('^(pesos|dolares)$'), tipo_envio),
                      MessageHandler(Filters.regex('^[+-]?([0-9]+([.][0-9]*)?|[.][0-9]+)$'), pedir_tasa),            
                     ],
            INPUT_N:[ MessageHandler(Filters.regex('^\d+$'), total_enviar)],

            INPUT_TEXT:[MessageHandler(Filters.text, input_string)]
        },
        
        fallbacks=[MessageHandler(Filters.text, inicio)]
    ))

    updater.start_polling()
    updater.idle()


 
