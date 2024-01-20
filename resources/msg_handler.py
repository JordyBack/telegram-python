import config
from resources import mysql_handler as mysql
from resources import lang_emojis as emoji
from common_functions import determine_user_language
import re
import datetime
import time
import arrow


def getReferrer(text):
    return text.split()[1] if len(text.split()) > 1 else None


def msg_type(message):
    if message.content_type == 'text':
        msg_type = message.text
    elif message.content_type == 'photo' or message.content_type == 'document':
        msg_type = message.caption
    return msg_type

def getUserID(message):
    if message.reply_to_message.content_type == 'text':
        user_id = int(message.reply_to_message.text.split('(#id')[1].split(')')[0])
    elif message.reply_to_message.content_type == 'photo' or message.reply_to_message.content_type == 'document':
        user_id = int(message.reply_to_message.caption.split('(#id')[1].split(')')[0])
    return user_id


def msgCheck(message):
    if message.reply_to_message.content_type == 'text':
        msg_check = message.reply_to_message.text
    elif message.reply_to_message.content_type == 'photo' or message.reply_to_message.content_type == 'document':
        msg_check = message.reply_to_message.caption
    return msg_check


def msgCaption(message):
    if message.caption == None:
        msgCaption = ''
    else:
        msgCaption = message.caption
    return msgCaption


# Gestion (Support - Utilisateur)
def snd_handler(user_id, bot, message, txt):
    try:
        if message.content_type == 'text':
            bot.send_chat_action(user_id, 'typing')
            bot.send_message(user_id, \
                             config.text_messages['support_response'].format(
                                 bot.get_chat(user_id).first_name) + f'\n\n{message.text}', parse_mode='Markdown',
                             disable_web_page_preview=True)

        elif message.content_type == 'photo':
            bot.send_chat_action(user_id, 'upload_photo')
            bot.send_photo(user_id, message.photo[-1].file_id,
                           caption=config.text_messages['support_response'].format(
                               bot.get_chat(user_id).first_name) + f'\n\n{msgCaption(message)}',
                           parse_mode='Markdown')

        elif message.content_type == 'document':
            bot.send_chat_action(user_id, 'upload_document')
            bot.send_document(user_id, message.document.file_id,
                              caption=config.text_messages['support_response'].format(
                                  bot.get_chat(user_id).first_name) + f'\n\n{msgCaption(message)}',
                              parse_mode='Markdown')
        else:
            pass

    except Exception as e:
        print(e)
        bot.reply_to(message, '❌ Ce format n\'est pas pris en charge et ne sera pas transféré.')
        return


# Gestion (Utilistayer - Support)
def fwd_handler(user_id, bot, message):
    try:
        print(f"Debug: Inside fwd_handler - user_id: {user_id}, bot: {bot}, message: {message}")
        mysql.spam(message.chat.id)
        user_language = determine_user_language(user_id)
        lang_emoji = emoji.lang_emoji(message.from_user.language_code)

        if message.content_type == 'text':
            if user_language == 'en':
                msg = bot.send_message(config.support_chat, "[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                    message.from_user.first_name,
                    ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                    message.from_user.id, lang_emoji, message.text), parse_mode='Markdown', disable_web_page_preview=True)
            else:
                msg = bot.send_message(config.support_chat, "[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                    message.from_user.first_name,
                    ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                    message.from_user.id, lang_emoji, message.text), parse_mode='Markdown', disable_web_page_preview=True)

        elif message.content_type == 'photo':
            if user_language == 'en':
                msg = bot.send_photo(config.support_chat, message.photo[-1].file_id,
                                     caption="[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                                         message.from_user.first_name,
                                         ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                                         message.from_user.id, lang_emoji, msgCaption(message)), parse_mode='Markdown')
            else:
                msg = bot.send_photo(config.support_chat, message.photo[-1].file_id,
                                     caption="[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                                         message.from_user.first_name,
                                         ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                                         message.from_user.id, lang_emoji, msgCaption(message)), parse_mode='Markdown')

        elif message.content_type == 'document':
            if user_language == 'en':
                msg = bot.send_document(config.support_chat, message.document.file_id,
                                        caption="[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                                            message.from_user.first_name,
                                            ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                                            message.from_user.id, lang_emoji, msgCaption(message)), parse_mode='Markdown')
            else:
                msg = bot.send_document(config.support_chat, message.document.file_id,
                                        caption="[{0}{1}](tg://user?id={2}) (#id{2}) | {3}\n\n{4}".format(
                                            message.from_user.first_name,
                                            ' {0}'.format(message.from_user.last_name) if message.from_user.last_name else '',
                                            message.from_user.id, lang_emoji, msgCaption(message)), parse_mode='Markdown')

        elif message.content_type == 'sticker':
            msg = bot.send_sticker(user_id, message.sticker.file_id)

        else:
            if user_language == 'en':
                bot.reply_to(message, '❌ This format is not supported and will not be forwarded.')
            else:
                bot.reply_to(message, '❌ Ce format n\'est pas pris en charge et ne sera pas transféré.')

        channel_id = re.sub(r"-100(\S+)", r"\1", str(config.support_chat))
        message_id = msg.message_id
        message_link = f'https://t.me/c/{channel_id}/{message_id}'
        mysql.post_open_ticket(message_link, user_id)

    except Exception as e:
        print(e)
        raise

    return fwd_handler



def bad_words_handler(bot, message):
    if config.bad_words_toggle:
        try:
            user_language = determine_user_language(message.from_user.id)
            if re.findall(config.regex_filter['bad_words'], msg_type(message)):
                if user_language == 'en':
                    bot.reply_to(message, '❗️ Watch your language...')
                else:
                    bot.reply_to(message, '❗️ Attention à ce que tu dis...')
                return bad_words_handler
        except Exception as e:
            pass


def time_zone():
    current_time = arrow.now(config.time_zone).strftime('%I:%M %p')
    return current_time


def repo(lang='fr'):
    if lang == 'en':
        msg = '\n\n[» Customer Review](https://t.me/+A06WtqsIiiYwODk0) ⭐️\n\n'
    else:
        msg = '\n\n[» Avis client](https://t.me/+A06WtqsIiiYwODk0) ⭐️\n\n'
    return msg

def spam_handler_warning(bot, user_id, message):
    if config.spam_toggle:
        ticket_spam = mysql.user_tables(user_id)['open_ticket_spam']
        if ticket_spam > config.spam_protection:
            user_language = determine_user_language(user_id)
            if user_language == 'en':
                warning_message = '{}, your messages are no longer being forwarded. Please wait until the team responds. Thank you.\n\n' \
                                  f'_Support local time is_ `{current_time}`.'.format(message.from_user.first_name)
            else:
                warning_message = '{}, vos messages ne sont plus transmis. Veuillez patienter jusqu\'à ce que l\'équipe réponde. Merci.\n\n' \
                                  f'_L\'heure locale du support est_ `{current_time}`.'.format(message.from_user.first_name)

            bot.reply_to(message, warning_message, parse_mode='Markdown')
            return spam_handler_warning


def spam_handler_blocked(bot, user_id, message):
    if config.spam_toggle:
        ticket_spam = mysql.user_tables(user_id)['open_ticket_spam']
        user_language = determine_user_language(user_id)    
        if ticket_spam > config.spam_protection:
            if user_language == 'en':
                warning_message = '{}, your messages are no longer being forwarded. Please wait until the team responds. Thank you.\n\n' \
                                  f'_Support local time is_ `{current_time}`.'.format(message.from_user.first_name)
            else:
                warning_message = '{}, vos messages ne sont plus transmis. Veuillez patienter jusqu\'à ce que l\'équipe réponde. Merci.\n\n' \
                                  f'_L\'heure locale du support est_ `{current_time}`.'.format(message.from_user.first_name)

            bot.reply_to(message, warning_message, parse_mode='Markdown')
            return spam_handler_blocked

current_time = time_zone()
