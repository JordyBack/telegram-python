import config
import pymysql
import telebot
import types
import arrow
import logging
import time

# Gestionnaire MySQL, Markups, Message
from resources import mysql_handler as mysql
from resources import markups_handler as markups
from resources import msg_handler as msg

from common_functions import get_user_package_info
from common_functions import determine_user_language

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from logging import StreamHandler
from datetime import datetime

bot = telebot.TeleBot(config.token)
channel_username = '@spliptv'

mysql.createTables

user_packages = {}
user_languages = {}

def update_user_language(user_id, language):
    config.user_sessions[user_id] = {'language': language}

# Support commande temporaire
@bot.message_handler(commands=['chatid'])
def send_chat_id(message):
    chat_id = message.chat.id
    bot.reply_to(message, f"🆔 L'ID de ce chat est : {chat_id}")


# Gestion Callback
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    try:
        logging.info("[📞] Callback reçu: %s", call.data)
        user_id = call.from_user.id
        user_language = determine_user_language(user_id)
        
        if call.data == 'EnglishCallbackdata':
            update_user_language(user_id, 'en')
            user_language = 'en'
            logging.info("[🇺🇸 / 🇬🇧] %s a changé la langue.", user_id)
            start_text_dict = config.text_messages.get('start', {})  
            start_text = start_text_dict.get(user_language, '')  
            markup = markups.create_start_markup_en()
            bot.send_message(user_id, start_text + msg.repo(lang='en'), parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
        else:
            markup = markups.create_start_markup_fr()

        if call.data == 'FrenchCallbackdata':
            update_user_language(user_id, 'fr')
            user_language = 'fr'
            logging.info("[🇫🇷] %s a changé la langue.", user_id)
            start_text_dict = config.text_messages.get('start', {})  
            start_text = start_text_dict.get(user_language, '')  
            markup = markups.create_start_markup_fr()
            bot.send_message(user_id, start_text + msg.repo(lang='fr'), parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
        else:
            markup = markups.create_start_markup_fr()

        if call.data == 'helpCallbackdata':
            user_language = determine_user_language(user_id)
            help_text_dict = config.text_messages.get('help', {})  
            help_text = help_text_dict.get(user_language, '')  
            bot.send_message(user_id, help_text, parse_mode='Markdown', disable_web_page_preview=True)

        elif call.data == 'yearCallbackdata':
            user_language = determine_user_language(user_id)
            markup = markups.create_screen_choice_markup(user_language)
            package_duration = '1 an'
            user_packages[user_id] = {'package_duration': package_duration}
            print(f"Updated user_packages for user {user_id}: {user_packages[user_id]}")
            year_text_dict = config.text_messages.get('year', {})  
            year_text = year_text_dict.get(user_language, '')  
            bot.send_message(user_id, year_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

        elif call.data in ['semesterCallbackdata', 'quarterCallbackdata']:
            user_language = determine_user_language(user_id)
            if call.data == 'semesterCallbackdata':
                package_duration = '6 mois'
                user_packages[user_id] = {'package_duration': package_duration}
                print(f"Updated user_packages for user {user_id}: {user_packages[user_id]}")
                text_key = 'semester'
            elif call.data == 'quarterCallbackdata':
                text_key = 'quarter'
                package_duration = '3 mois'
                user_packages[user_id] = {'package_duration': package_duration}
                print(f"Updated user_packages for user {user_id}: {user_packages[user_id]}")
            month_text_dict = config.text_messages.get(text_key, {})
            month_text = month_text_dict.get(user_language, '')
            markup = markups.create_payment_markup(user_language)
            bot.send_message(user_id, month_text, reply_markup=markup, parse_mode='Markdown', disable_web_page_preview=True)

        elif call.data in ['oneScreenCallbackdata', 'twoScreensCallbackdata', 'threeScreensCallbackdata']:
            user_language = determine_user_language(user_id)
            screen_choice_mapping = {
                'oneScreenCallbackdata': {'fr': '1 écran pour un montant total de 60 euros', 'en': '1 screen for a total amount of 60 euros'},
                'twoScreensCallbackdata': {'fr': '2 écrans pour un montant total de 95 euros', 'en': '2 screens for a total amount of 95 euros'},
                'threeScreensCallbackdata': {'fr': '3 écrans pour un montant total de 125 euros', 'en': '3 screens for a total amount of 125 euros'},
            }
            if call.data in screen_choice_mapping:
                chosen_option = screen_choice_mapping[call.data]
                package_duration = '1 an'  # Replace this with the actual logic to determine the package duration
                package_screen = chosen_option['fr']  # You can choose either 'fr' or 'en' based on user's language
                user_packages[user_id] = {'package_duration': package_duration, 'package_screen': package_screen}
                print(f"Updated user_packages for user {user_id}: {user_packages[user_id]}")
            user_choice_key = call.data
            user_choice = screen_choice_mapping[user_choice_key][user_language]
            screen_choice_text = config.text_messages['screen_choice'][user_language].format(user_choice)
            markup = markups.create_payment_markup(user_language)
            bot.send_message(user_id, screen_choice_text, parse_mode='Markdown', reply_markup=markup)
        
        elif call.data.startswith('method_'):
            payment_method = call.data.replace('method_', '')
            user_language = determine_user_language(user_id)
            payment_text = config.text_messages['payment'][user_language]
            markup = markups.create_payment_confirmation_markup(user_language)
            response_text = None
            if payment_method == 'bitcoin':
                response_text = config.text_messages['bitcoin_payment'][user_language]
            elif payment_method == 'paypal':
                response_text = config.text_messages['paypal_payment'][user_language]
            if response_text is not None:
                bot.send_message(user_id, response_text, parse_mode='Markdown', reply_markup=markup)
                print(f"Sent payment response to user {user_id} for {payment_method}.")

        elif call.data == 'payment_completed':
            default_values = {'package_duration': '1 an', 'package_screen': '1 écran pour un montant total de 60 euros'}
            user_packages.setdefault(user_id, default_values)
            support_group_chat_id = config.support_chat
            user_id = call.from_user.id
            user_package = user_packages.get(user_id, {'package_duration': '1 an', 'package_screen': '1 écran pour un montant total de 60 euros'})
            if 'package_screen' in user_package:
                screens_info = f" with {user_package['package_screen']} screen(s)"
            else:
                screens_info = " 1 écran"
            print(f"User {user_id} completed payment for {user_package['package_duration']}{screens_info}.")
            user_username = call.from_user.username
            alert_text = f"⚠️ Paiement effectué par l'utilisateur {user_username} ({user_id}) pour le forfait {user_packages[user_id]['package_duration']}"
            if 'package_screen' in user_packages[user_id]:
                alert_text += f" avec {user_packages[user_id]['package_screen']}"
            alert_text += " ! Assistance requise. ⚠️"         
            bot.send_message(support_group_chat_id, alert_text)
            print(f"Sent payment alert to support group.")
            user_language = determine_user_language(user_id)
            confirmation_text_dict = config.text_messages.get('payment_confirmation', {})
            confirmation_text = confirmation_text_dict.get(user_language, 'Paiement effectué ! Un agent du support vous assistera sous peu.')
            print(f"Confirmation text: {confirmation_text}")  
            try:
                bot.send_message(user_id, confirmation_text)
                print(f"Sent payment confirmation to user {user_id}.")
            except Exception as e:
                print(f"Error sending confirmation message to user {user_id}: {e}")

    except Exception as e:
        print(f"An error occurred in callback handler: {e}")
        bot.reply_to(call.message, '❌ Une erreur s\'est produite. Veuillez réessayer plus tard.')
        return

# Envoie du message /start en privée et /startcanal pour le canal
@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id
        user_language = determine_user_language(user_id)
        if user_language == 'en':
            markup = markups.create_start_markup_en()
        else:
            markup = markups.create_start_markup_fr()
        start_text_dict = config.text_messages.get('start', {})  
        start_text = start_text_dict.get(user_language, '')  
        bot.send_message(message.chat.id, start_text.format(message.from_user.first_name) + msg.repo(lang=user_language),
                         parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
        mysql.start_bot(message.chat.id)
    else:
        channel_id = '@spliptv'
        start_text_dict_channel = config.text_messages.get('start', {})
        start_text_channel = start_text_dict_channel.get('fr', '')  
        bot.send_message(channel_id,
                         start_text_channel.format(message.from_user.first_name) + msg.repo(),
                         parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
        mysql.start_bot(channel_id)

@bot.message_handler(commands=['startcanal'])
def test_command(message):
    jordy_user_id = 703053891  
    if message.from_user.id == jordy_user_id:
        markup = markups.create_start_markup_fr()
        start_text_dict_channel = config.text_messages.get('start', {})
        start_text_channel = start_text_dict_channel.get('fr', '')  
        channel_id = '-1001938737257'
        logging.info("[✅] Envoi du message de démarrage au canal.")
        bot.send_message(channel_id,
                         start_text_channel.format(message.from_user.first_name) + msg.repo(),
                         parse_mode='Markdown', disable_web_page_preview=True, reply_markup=markup)
    else:
        bot.send_message(
            message.chat.id,
            "Vous n'avez pas la permission d'exécuter cette commande."
        )

# Liste ticket 
@bot.message_handler(commands=['tickets', 't'])
def ot_handler(message):
    if message.chat.id == config.support_chat:
        if not mysql.open_tickets:
            bot.reply_to(message, "ℹ️ Super travail, vous avez répondu à tous vos tickets !")
            return
            
        ot_msg = '📨 *Tickets ouverts:*\n\n'
        for user in mysql.open_tickets:
            bot.send_chat_action(message.chat.id, 'typing')
            ot_link = mysql.user_tables(int(user))['open_ticket_link']

            now = arrow.now()
            diff = datetime.now() - mysql.user_tables(int(user))['open_ticket_time']
            diff.total_seconds() / 3600  # seconds to hour
            time_since_secs = float(diff.seconds)
            time_since = now.shift(seconds=-time_since_secs).humanize()

            # Bring attention to 1 day old tickets
            if time_since_secs > config.open_ticket_emoji * 3600:
                alert = ' ↳ ⚠️ '
            else:
                alert = ' ↳ '

            ot_msg += "• [{0}{1}](tg://user?id={2}) (`{2}`)\n{5}_{3}_ [↪️ Aller au message.]({4})\n".format(
                bot.get_chat(int(user)).first_name,
                ' {0}'.format(bot.get_chat(int(user)).last_name) if bot.get_chat(int(user)).last_name else '',
                int(user), time_since, ot_link, alert)

        bot.send_message(message.chat.id, ot_msg, parse_mode='Markdown')
    else:
        pass

# Fermer ticket
@bot.message_handler(commands=['close', 'c'])
def ot_handler(message):
    if message.chat.id == config.support_chat:
        if message.reply_to_message and '(#id' in message.reply_to_message.text:
            bot.send_chat_action(message.chat.id, 'typing')
            user_id = int(message.reply_to_message.text.split('(#id')[1].split(')')[0])
            ticket_status = mysql.user_tables(user_id)['open_ticket']

            if ticket_status == 0:
                bot.reply_to(message, '❌ Cet utilisateur n\'a pas de ticket ouvert...')
            else:
                mysql.reset_open_ticket(user_id)                
                user_language = determine_user_language(user_id)
                if user_language == 'en':
                    bot.reply_to(message, '✅ Ok, j\'ai fermé ce ticket utilisateur !')
                    support_message = "Your ticket has been closed by support."
                    bot.send_message(user_id, support_message)
                else:
                    bot.reply_to(message, '✅ Ok, j\'ai fermé ce ticket utilisateur !')
                    support_message = "Votre ticket a été fermé par le support."
                    bot.send_message(user_id, support_message)
        else:
            bot.reply_to(message, 'ℹ️ Vous devrez répondre à un message')
    else:
        pass


# Liste ban
@bot.message_handler(commands=['banned'])
def ot_handler(message):
    if message.chat.id == config.support_chat:
        if not mysql.banned:
            bot.reply_to(message, "ℹ️ Bonne nouvelle, personne n'a été banni... pour l'instant.")
            return

        ot_msg = '⛔️ *Utilisateurs bannis :*\n\n'
        for user in mysql.banned:
            bot.send_chat_action(message.chat.id, 'typing')
            ot_link = mysql.user_tables(int(user))['open_ticket_link']

            ot_msg += "• [{0}{1}](tg://user?id={2}) (`{2}`)\n[➜ Aller au dernier message]({3})\n".format(
                bot.get_chat(int(user)).first_name,
                ' {0}'.format(bot.get_chat(int(user)).last_name) if bot.get_chat(int(user)).last_name else '',
                int(user), ot_link)

        bot.send_message(message.chat.id, ot_msg, parse_mode='Markdown')
    else:
        pass


# Ban commande
@bot.message_handler(commands=['ban'])
def ot_handler(message):
    try:
        if message.chat.id == config.support_chat:
            if message.reply_to_message and '(#id' in msg.msgCheck(message):
                user_id = msg.getUserID(message)
                banned_status = mysql.user_tables(user_id)['banned']

                if banned_status == 1:
                    bot.reply_to(message, '❌ Utilisateur déjà banni...')
                else:
                    mysql.ban_user(user_id)
                    try:
                        mysql.reset_open_ticket(user_id)
                    except Exception as e:
                        pass
                    bot.reply_to(message, '✅ Utilisateur banni!')

            elif msg.getReferrer(message.text):
                user_id = int(msg.getReferrer(message.text))
                banned_status = mysql.user_tables(user_id)['banned']

                if banned_status == 1:
                    bot.reply_to(message, '❌ Utilisateur déjà banni...')
                else:
                    mysql.ban_user(user_id)
                    try:
                        mysql.reset_open_ticket(user_id)
                    except Exception as e:
                        pass
                    bot.reply_to(message, '✅ Utilisateur banni!')
        else:
            bot.reply_to(message, 'ℹ️ Vous devrez soit répondre à un message, soit mentionner un « ID utilisateur ».',
                         parse_mode='Markdown')
    except TypeError:
        bot.reply_to(message, '❌ Êtes-vous sûr d\'avoir déjà interagi avec cet utilisateur... ?')


# Un-ban commande
@bot.message_handler(commands=['unban'])
def ot_handler(message):
    try:
        if message.chat.id == config.support_chat:
            if message.reply_to_message and '(#id' in msg.msgCheck(message):
                user_id = msg.getUserID(message)
                banned_status = mysql.user_tables(user_id)['banned']

                if banned_status == 0:
                    bot.reply_to(message, '❌ Cet utilisateur est déjà débanni...')
                else:
                    mysql.unban_user(user_id)
                    bot.reply_to(message, '✅ Ok, cet utilisateur est débanni !')

            elif msg.getReferrer(message.text):
                user_id = int(msg.getReferrer(message.text))
                banned_status = mysql.user_tables(user_id)['banned']

                if banned_status == 0:
                    bot.reply_to(message, '❌ Cet utilisateur est déjà débanni...')
                else:
                    mysql.unban_user(user_id)
                    bot.reply_to(message, '✅ Ok, cet utilisateur est débanni !')
            else:
                bot.reply_to(message, 'ℹ️ Vous devrez soit répondre à un message, soit mentionner l\'identifiant d\'un utilisateur.',
                             parse_mode='Markdown')
    except TypeError:
        bot.reply_to(message, '❌ Êtes-vous sûr d\'avoir déjà interagi avec cet utilisateur...?')

# Gestion message (Utilisateur - Support)
@bot.message_handler(func=lambda message: message.chat.type == 'private', content_types=['text', 'photo', 'document'])
def echo_all(message):
    while True:
        mysql.start_bot(message.chat.id)
        user_id = message.chat.id
        message = message
        banned = mysql.user_tables(user_id)['banned']
        ticket_status = mysql.user_tables(user_id)['open_ticket']
        ticket_spam = mysql.user_tables(user_id)['open_ticket_spam']
        if banned == 1:
            return
        elif msg.spam_handler_warning(bot, user_id, message):
            return
        elif msg.bad_words_handler(bot, message):
            return
        elif msg.spam_handler_blocked(bot, user_id, message):
            return
        elif ticket_status == 0:
            mysql.open_ticket(user_id)
            continue
        else:
            msg.fwd_handler(user_id, bot, message)
            return

# Gestion message (Support - Utilisateur)
@bot.message_handler(content_types=['text', 'photo', 'document'])
def echo_all(message):
    while True:
        try:
            try:
                user_id = msg.getUserID(message)
                message = message
                text = message.text 
                msg_check = msg.msgCheck(message)
                ticket_status = mysql.user_tables(user_id)['open_ticket']
                banned_status = mysql.user_tables(user_id)['banned']

                if banned_status == 1:
                    mysql.unban_user(user_id)
                    bot.reply_to(message, 'ℹ️ *Note : Cet utilisateur était banni.*\n_Débanni et message envoyé !_',
                                 parse_mode='Markdown')

                elif ticket_status == 1:
                    mysql.reset_open_ticket(user_id)
                    continue
                else:
                    if message.reply_to_message and '(#id' in msg_check:
                        msg.snd_handler(user_id, bot, message, text)
                        return

            except telebot.apiaideer.ApiException:
                bot.reply_to(message, '❌ Je n\'ai pas pu envoyer ce message...\nL\'utilisateur m\'a peut-être bloqué.')
                return
        except Exception as e:
            bot.reply_to(message, '❌ Commande invalide !')
            return 

# Fonction pour récupérer les membres du canal
def get_channel_members(channel_username):
    try:
        members_count = bot.get_chat_members_count(channel_username)
        return members_count
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des membres du canal : {e}")
        return None

# Fonction pour afficher les membres du canal
def log_channel_members(channel_username):
    try:
        members_count = get_channel_members(channel_username)
        if members_count is not None:
            logging.info(f"[👥] Nombre total de membres dans le canal {channel_username}: {members_count} Abonnés.")
        else:
            logging.error("Erreur lors de la récupération des membres du canal.")
    except Exception as e:
        logging.error(f"Erreur lors de la récupération des membres du canal : {e}")

# Gestion lancement du bot ! 
if __name__ == "__main__":
    time.sleep(1)
    print("Démarrage du bot...")
    time.sleep(3)
    logging.info("[✅] SPL IPTV BOT")
    log_channel_members('@spliptv') #-1001938737257
    print("=====================================================================")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error("Une erreur s'est produite : %s", e)
