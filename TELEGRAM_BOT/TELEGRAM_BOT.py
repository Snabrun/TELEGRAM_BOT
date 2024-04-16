import telebot
from telebot import types
import requests
import json
from datetime import datetime
import time
import schedule

bot = telebot.TeleBot("7085433359:AAETrss2V6vHve7eAQKRi3QgXs9m5DLehJs")

@bot.message_handler(commands=['start', 'back'])    
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_news = types.InlineKeyboardButton('Helldivers news', callback_data='delete')
    markup.add(btn_news)
    bot.send_message(message.chat.id, 'Hello soldier!', reply_markup=markup)



@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Last news')
        res = requests.get('https://helldiverstrainingmanual.com/api/v1/war/news')
        data = json.loads(res.text)
        for news_item in data:
            published_time = datetime.utcfromtimestamp(news_item["published"])
            formatted_time = published_time.strftime("%H:%M:%S")
            bot.send_message(callback.message.chat.id, f'Published: {formatted_time}\n{news_item["message"]}')
            


last_processed_id = 2805  # Инициализация переменной для хранения последнего обработанного ID

@bot.message_handler(func=lambda message: message.text.lower() == 'ebash')
def handle_start(message):
    # Запускаем выполнение планировщика после получения сообщения "start" от пользователя
        #schedule.every(30).minutes.do(check_api(message))
        while True:
            
            check_api(message)
            time.sleep(30)


def check_api(message):
    global last_processed_id  # Объявляем переменную как глобальную, чтобы иметь доступ к ней из функции
    res = requests.get('https://helldiverstrainingmanual.com/api/v1/war/news')
    data = json.loads(res.text)
    for news_item in data:
        if news_item["id"] > last_processed_id:
            bot.send_message(message.chat.id, 'Hello soldier!')
            last_processed_id = news_item["id"]
            published_time = datetime.utcfromtimestamp(news_item["published"])
            formatted_time = published_time.strftime("%H:%M:%S")
            bot.send_message(message.chat.id, f'Published: {formatted_time}\n{news_item["message"]}')
            




bot.infinity_polling()
