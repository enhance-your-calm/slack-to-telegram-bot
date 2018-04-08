import os
import telebot
import dotenv
from threading import Thread

from slack_bot import SlackBot

dotenv.load_dotenv(dotenv.find_dotenv())
telegram_token = os.getenv('TELEGRAM_TOKEN')
tg_bot = telebot.TeleBot(telegram_token)
tg_bot.handlers = {}


@tg_bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    tg_bot.reply_to(message, """\
Для начала работы отправьте /bind <slack_token>
Получить slack_token: https://api.slack.com/custom-integrations/legacy-tokens 
(нажать "Create token")
""")


# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@tg_bot.message_handler(commands=['echo'], func=lambda message: True)
def echo_message(message):
    tg_bot.reply_to(message, message.text)


@tg_bot.message_handler(commands=['bind'])
def run_slack_bot_worker(message):
    print(message)
    if message.chat.id in tg_bot.handlers:
        tg_bot.send_message(message.chat.id, "Already listen. use /unbind")
    try:
        slack_token = message.text.split(' ')[1]
    except IndexError:
        tg_bot.send_message(message.chat.id, "token is empty")
    else:
        slack_bot = SlackBot(token=slack_token, telegram_bot=tg_bot, telegram_chat_id=message.chat.id)
        _th = Thread(target=slack_bot.listen)
        tg_bot.handlers[message.chat.id] = _th
        _th.start()
        tg_bot.send_message(message.chat.id, "ok. listen your slack ...")


@tg_bot.message_handler(commands=['unbind'])
def remove_slack_bot_worker(message):
    if message.chat.id in tg_bot.handlers:
        del tg_bot.handlers[message.chat.id]
        tg_bot.send_message(message.chat.id, "ok")
    else:
        tg_bot.send_message(message.chat.id, "no binding found")


tg_bot.polling()
