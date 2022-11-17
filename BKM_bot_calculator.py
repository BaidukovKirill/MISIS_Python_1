import telebot
from telebot import types
import re

bot = telebot.TeleBot('API KEY IS HERE')

expression = ''
prev_expression = ''

keyboard = types.InlineKeyboardMarkup()

keyboard.row(
    types.InlineKeyboardButton(text = '(', callback_data='('),
    types.InlineKeyboardButton(text = ')', callback_data=')'),
    types.InlineKeyboardButton(text='⌫', callback_data='⌫'),
    types.InlineKeyboardButton(text = 'CLEAR', callback_data='CLEAR')

)
keyboard.row(
    types.InlineKeyboardButton(text = '7', callback_data='7'),
    types.InlineKeyboardButton(text = '8', callback_data='8'),
    types.InlineKeyboardButton(text = '9', callback_data='9'),
    types.InlineKeyboardButton(text = '/', callback_data='/')
)
keyboard.row(
    types.InlineKeyboardButton(text = '4', callback_data='4'),
    types.InlineKeyboardButton(text = '5', callback_data='5'),
    types.InlineKeyboardButton(text = '6', callback_data='6'),
    types.InlineKeyboardButton(text = '*', callback_data='*')
)
keyboard.row(
    types.InlineKeyboardButton(text = '1', callback_data='1'),
    types.InlineKeyboardButton(text = '2', callback_data='2'),
    types.InlineKeyboardButton(text = '3', callback_data='3'),
    types.InlineKeyboardButton(text = '-', callback_data='-')
)
keyboard.row(
    types.InlineKeyboardButton(text = '0', callback_data='0'),
    types.InlineKeyboardButton(text = '.', callback_data='.'),
    types.InlineKeyboardButton(text = '=', callback_data='='),
    types.InlineKeyboardButton(text = '+', callback_data='+')
)

@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Напиши мне какое-нибудь математическое выражение, а я постараюсь его посчитать')

@bot.message_handler(content_types=["text"])
def handle_text(message):

    user_input = message.text
    if user_input =='/my_friends':
        keyboard_friends = types.InlineKeyboardMarkup()

        key_text = types.InlineKeyboardButton(text='Text Analyzer', url = 'https://t.me/BKM_TextAnalyzerBot')
        keyboard_friends.add(key_text)
        key_site = types.InlineKeyboardButton(text='Site Availability', url = 'https://t.me/BKM_SiteAvailabilityBot')
        keyboard_friends.add(key_site)
        bot.send_message(message.from_user.id, 'Подпишись на моих друзей, пожауйста',reply_markup=keyboard_friends)

    elif user_input =='/calculator':
        global expression
        if expression == '':
            bot.send_message(message.from_user.id, text='0', reply_markup=keyboard)
        else:
            bot.send_message(message.from_user.id, text=expression, reply_markup=keyboard)


    else:
        try:
            result = eval(user_input)
            to_write_back = f'{user_input} = {result}'
            bot.send_message(message.chat.id, f'Вот решение {to_write_back}')
        except:
            to_write_back = 'Oops...'
            bot.send_message(message.chat.id, f'{to_write_back}')

@bot.callback_query_handler(func=lambda call: True)
def callback_func(query):
    global expression, prev_expression
    data = query.data
    if data == 'CLEAR':
        expression = ''
    elif data =='⌫':
        if expression!='':
            expression = expression[:-1]
    elif data == '=':
        try:
            expression = str(eval(expression))
        except:
            expression = 'Oops...'

    else:
        expression+=data


    if expression =='':
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text = '0', reply_markup=keyboard)
        prev_expression = '0'
    else:
        bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=expression, reply_markup=keyboard)
        prev_expression = expression
    if expression == 'Oops...':
        expression = ''
bot.polling(none_stop=True, interval=0)