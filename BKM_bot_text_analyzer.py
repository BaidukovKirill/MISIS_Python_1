import telebot
from telebot import types
import emoji
import re

bot = telebot.TeleBot('API KEY IS HERE')

def tokenize(some_text):
    basic_to_reaplace = ['.',',','?','!',';',':', '\n']
    for elem in basic_to_reaplace:
        some_text = some_text.replace(elem, ' ')
    tokenized = some_text.split(' ')
    tokenized = [word for word in tokenized if word != '']
    return tokenized

def unique_words_count(some_text):
    tokenized = tokenize(some_text)
    tokenized_lower = [word.lower() for word in tokenized]
    unique_words = set(tokenized_lower)
    return len(unique_words)

def count_sentences(some_text):
    new_text = re.sub(r'[.!?]\s', r'|', some_text)
    sent_num = len(new_text.split('|'))
    return sent_num

def popular_words(some_text):
    popular_words=[]

    tokenized = tokenize(some_text)
    tokenized_lower = [word.lower() for word in tokenized]
    tokenized_dict = dict.fromkeys(tokenized_lower)

    for token in tokenized_lower:
        tokenized_dict[token] = tokenized_lower.count(token) / len(tokenized_lower) * 100

    to_drop_arr = ['без' , 'в' , 'до' , 'для' , 'за' , 'из' , 'к' , 'на' , 'над' , 'о' , 'об' , 'от' , 'по' , 'под' , 'пред ,' 'при' , 'про' , 'с' , 'у' , 'через',
               'а ,' 'и' , 'чтобы' , 'если',
               'но', 'или', 'либо', 'что', 'хотя', 'будто', 'ли',
               ]

    for to_drop in to_drop_arr:
        if to_drop in tokenized_dict.keys():
            tokenized_dict.pop(to_drop)

    max_freq_word = max(tokenized_dict, key = tokenized_dict.get)

    for key in tokenized_dict.keys():
        if tokenized_dict[key]==tokenized_dict[max_freq_word]:
            popular_words.append(key)

    return popular_words

def text_processing(some_text):
    text_length = 0
    unique_counter = 0
    popular_words_list = []
    number_of_sentences = 0

    text_length = len(some_text)
    unique_counter = unique_words_count(some_text)
    number_of_sentences = count_sentences(some_text)
    popular_words_list = popular_words(some_text)
    popular_words_string = ''
    for i in range(len(popular_words_list)):
        if i!=len(popular_words_list)-1:
            popular_words_string+=f'{popular_words_list[i]}, '
        else:
            popular_words_string+=popular_words_list[i]

    return text_length,number_of_sentences,unique_counter,popular_words_string



@bot.message_handler(commands=["start"])
def start(m, res=False):
    bot.send_message(m.chat.id, 'Привет! Напиши мне какой нибудь текст')




@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text=='/info':
        bot.send_message(message.chat.id, emoji.emojize('Привет! На связи бот для просто анализа текста! :desktop_computer:\nВведите текст для анализа'))

    elif message.text=='/surprize':
        bot.send_message(message.chat.id, emoji.emojize('Сюрприз! С твоего счёта спишется 100 eur :euro_banknote:'))
    elif message.text =='/my_friends':
        keyboard = types.InlineKeyboardMarkup()

        key_calc = types.InlineKeyboardButton(text='Calculator', url = 'https://t.me/BKM_CalculatorBot')
        keyboard.add(key_calc)
        key_site = types.InlineKeyboardButton(text='Site Availability', url = 'https://t.me/BKM_SiteAvailabilityBot')
        keyboard.add(key_site)
        bot.send_message(message.from_user.id, 'Подпишись на моих друзей, пожауйста',reply_markup=keyboard)
    else:
        user_text = message.text

        text_length, number_of_sentences,unique_counter, popular_words_list= text_processing(user_text)

        bot.send_message(message.chat.id, f'Длина текста: {text_length}\nКоличество предложений: {number_of_sentences}\nЧисло уникальных слов: {unique_counter}\nСамые популярные слова: {popular_words_list}')






bot.polling(none_stop=True, interval=0)