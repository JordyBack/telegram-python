import config
import telebot
import sys
import os
base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(base_path)
from common_functions import determine_user_language
from resources import msg_handler as msg
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def create_start_markup_fr(lang='fr'):
    markup = InlineKeyboardMarkup()

    yearButton = InlineKeyboardButton('1 an 📅', callback_data='yearCallbackdata')
    semestreButton = InlineKeyboardButton('6 mois 📆', callback_data='semesterCallbackdata')
    trimestreButton = InlineKeyboardButton('3 mois ⏳', callback_data='quarterCallbackdata')
    helpButton = InlineKeyboardButton('Besoin d\'aide ❓', callback_data='helpCallbackdata')
    EnglishButton = InlineKeyboardButton('English 🇺🇸/🇬🇧', callback_data='EnglishCallbackdata')
    #addContactsButton = InlineKeyboardButton('Partager 📲', callback_data='addContactsCallbackdata')

    markup.add(yearButton)
    markup.row(semestreButton, trimestreButton)
    markup.add(helpButton)
    markup.row(EnglishButton)
    #markup.add(addContactsButton)

    return markup

def create_start_markup_en(lang='en'):
    markup = InlineKeyboardMarkup()

    yearButton = InlineKeyboardButton('1 year 📅', callback_data='yearCallbackdata')
    semesterButton = InlineKeyboardButton('6 month 📆', callback_data='semesterCallbackdata')
    quarterButton = InlineKeyboardButton('3 month ⏳', callback_data='quarterCallbackdata')
    helpButton = InlineKeyboardButton('Need help ❓', callback_data='helpCallbackdata')
    FrenchButton = InlineKeyboardButton('Français 🇫🇷', callback_data='FrenchCallbackdata')
    #addContactsButton = InlineKeyboardButton('Share 📲', callback_data='addContactsCallbackdata')

    markup.add(yearButton)
    markup.row(semesterButton, quarterButton)
    markup.add(helpButton)
    markup.row(FrenchButton)
    #markup.add(addContactsButton)

    return markup

def create_screen_choice_markup(lang='fr'):
    markup = telebot.types.InlineKeyboardMarkup()

    if lang == 'fr':
        options = [
            ('1 écran ⭐️', 'oneScreenCallbackdata'),
            ('2 écrans 🌟', 'twoScreensCallbackdata'),
            ('3 écrans ✨', 'threeScreensCallbackdata'),
        ]
    elif lang == 'en':
        options = [
            ('1 screen ⭐️', 'oneScreenCallbackdata'),
            ('2 screens 🌟', 'twoScreensCallbackdata'),
            ('3 screens ✨', 'threeScreensCallbackdata'),
        ]

    markup.row(*[telebot.types.InlineKeyboardButton(text, callback_data=data) for text, data in options])

    return markup

def create_payment_markup(lang='fr'):
    markup = telebot.types.InlineKeyboardMarkup()
    if lang == 'fr':
        options = [
            ('BitCoin', 'method_bitcoin'),  
            ('PayPal', 'method_paypal'),    
        ]
    elif lang == 'en':
        options = [
            ('BitCoin', 'method_bitcoin'),  
            ('PayPal', 'method_paypal'),  
        ]
    markup.row(*[telebot.types.InlineKeyboardButton(text, callback_data=data) for text, data in options])
    return markup

def create_payment_confirmation_markup(lang='fr'):
    markup = telebot.types.InlineKeyboardMarkup()    
    if lang == 'fr':
        button_text = 'Paiement effectué ✅'
    elif lang == 'en':
        button_text = 'Payment completed ✅'
    markup.row(telebot.types.InlineKeyboardButton(button_text, callback_data='payment_completed'))
    print(f"Created payment completion button with text: {button_text}")
    return markup
