import telebot
from telebot import types
import re

bot = telebot.TeleBot('API_KEY_IS_HERE')

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Напиши мне какое-нибудь математическое выражение, а я постараюсь его посчитать')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_input = message.text
    if user_input =='/my_friends':
        keyboard = types.InlineKeyboardMarkup()

        key_text = types.InlineKeyboardButton(text='Text Analyzer', url = 'https://t.me/BKM_TextAnalyzerBot')
        keyboard.add(key_text)
        key_site = types.InlineKeyboardButton(text='Site Availability', url = 'https://t.me/BKM_SiteAvailabilityBot')
        keyboard.add(key_site)
        bot.send_message(message.from_user.id, 'Подпишись на моих друзей, пожауйста',reply_markup=keyboard)

    else:
        try:
            result = eval(user_input)
            to_write_back = f'{user_input} = {result}'
            bot.send_message(message.chat.id, f'Вот решение {to_write_back}')
        except:
            to_write_back = 'Oops...'
            bot.send_message(message.chat.id, f'{to_write_back}')




bot.polling(none_stop=True, interval=0)