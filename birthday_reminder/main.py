import telebot
import json


def load_birthdays(): # Create and load a json file
    if not os.path.exists("bd.json"): 
        with open("bd.json", "w") as file:
            json.dump({}, file)  
    with open("bds.json", "r") as file:
        return json.load(file)  

def save_json(data): # save data to bd.json file
    with open("bd.json", "w") as file:
        json.dump(data, file)


birthdays = load_json()
user_data = {}
bot = telebot.TeleBot("")


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "welcome to birthday Bot! type /add to add a new birthday!")

@bot.message_handler(commands=["add"])
def instruct(message):
    bot.send_message(message.chat.id, "enter the name for the birthday")
    user_data[message.chat.id] = {}
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    global name
    name = message.text
    user_data[message.chat.id]["name"] = name
    bot.send_message(message.chat.id, f"type the birthday date for {name}! eg: DD/MM")
    bot.register_next_step_handler(message, get_date)

def get_date(message):
    global birthday_date
    birthday_date = message.text
    user_id = message.chat.id
    try:
        # Example of date validation (optional: use datetime for stricter checks)
        if len(birthday_date.split("/")) == 2:
            user_data[user_id]['date'] = birthday_date
            name = user_data[user_id]['name']
            birthdays[name] = birthday_date
            save_json(birthdays)
            bot.send_message(message.chat.id, f"Birthday for {name} on {birthday_date} has been saved!")
        else:
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Invalid date format. Please use DD/MM.")
        return

bot.infinity_polling()
