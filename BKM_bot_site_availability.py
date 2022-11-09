import telebot
from telebot import types
import urllib3

http = urllib3.PoolManager()
bot = telebot.TeleBot('API_KEY_HERE')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Пришли мне ссылку, а я тебе скажу доступен сайт или нет')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    try:
        r = http.request('GET', message.text)
        status = r.status
    except:
        status = -1

    if status == 200:
        bot.send_message(message.chat.id, f'Круто! Сайт {message.text} доступен!')
    elif status == 400:
        bot.send_message(message.chat.id, 'Bad request')
    elif status == 403:
        bot.send_message(message.chat.id, 'Forbidden')
    elif status == 404:
        bot.send_message(message.chat.id, 'Not Found')
    elif status == 500:
        bot.send_message(message.chat.id, 'Internal Server Error')
    elif status == 502:
        bot.send_message(message.chat.id, 'Bad Gateway')
    elif status == 503:
        bot.send_message(message.chat.id, 'Service Unavailable')
    elif status == 504:
        bot.send_message(message.chat.id, 'Gateway Timeout')
    elif status == 505:
        bot.send_message(message.chat.id, 'HTTP Version Not Supported')
    elif status == -1:
        bot.send_message(message.chat.id, 'Какая то странная ошибка...')
    else:
        bot.send_message(message.chat.id, 'Мне сложно, попробуй снова')

bot.polling(none_stop=True, interval=0)