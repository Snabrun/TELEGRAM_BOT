import telebot
from telebot import types

bot = telebot.TeleBot("7085433359:AAETrss2V6vHve7eAQKRi3QgXs9m5DLehJs")

@bot.message_handler(commands=['start', 'back'])    
def start(message):
    markup = types.InlineKeyboardMarkup()
    btn_news = types.InlineKeyboardButton('Helldivers news', callback_data='delete')
    markup.add(btn_news)
    bot.send_message(message.chat.id, 'Yo', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
        bot.delete_message(callback.message.chat.id, callback.message.message_id)
        bot.send_message(callback.message.chat.id, 'Last news')
        

bot.infinity_polling()
