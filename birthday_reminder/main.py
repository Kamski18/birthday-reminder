import telebot

bot = telebot.TeleBot("API_KEY")

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "welcome to birthday Bot! type /add to add a new birthday!")

@bot.message_handler(commans=["add"])
def instruct(message):
    bot.send_message(message.chat.id, "enter the name for the birthday")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    bot.send_message(message.chat.id, f"type the birthday date for {name}!")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    global birthday_date
    birthday_date = message.text
    # masukkan data dalam database
    #if success ckp success, klau tak bot state ade prob (specific prob klau boleh)

bot.infinity_polling()
