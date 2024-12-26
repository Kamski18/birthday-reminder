import telebot
import json
import os
from datetime import datetime

def load_json():
    if not os.path.exists("bd.json"):  # Check if file exists
        with open("bd.json", "w") as file:
            json.dump({}, file)  # Create a new json file 
    
    
    if os.path.getsize("bd.json") == 0: # Check if the file is empty
        with open("bd.json", "w") as file:
            json.dump({}, file) 

    with open("birthdays.json", "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}
    

def save_json(data): # save data to bd.json file
    with open("bd.json", "w") as file:
        json.dump(data, file)



birthdays = load_json()
user_data = {}



bot = telebot.TeleBot("7947700211:AAEagVGIM3oSk23lvTbbaBzn74TVL8Bvfg0")



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
    if "/" not in name:
        user_data[message.chat.id]["name"] = name
        bot.send_message(message.chat.id, f"type the birthday date for {name}! eg: DD/MM")
        bot.register_next_step_handler(message, get_date)
        
    else:
        bot.send_message(message.chat.id, "Sorry but name cannot contain / symbol!")
    

def get_date(message):
    user_id = message.chat.id
    date = message.text

    try:
        
        current_year = datetime.now().year
        date_with_year = f"{current_year}-{date}"


        parsed_date = datetime.strptime(date_with_year, "%Y-%d/%m")
        
        name = user_data[user_id]['name']
        if str(user_id) not in birthdays:
            birthdays[str(user_id)] = {}
        birthdays[str(user_id)][name] = parsed_date.strftime("%d/%m")  
        save_json(birthdays)
        bot.send_message(message.chat.id, f"Birthday for {name} on {parsed_date.strftime('%d/%m')} has been saved!")
    except ValueError:
        
        bot.send_message(message.chat.id, "Invalid date format. Please use DD/MM. Try again.")
        bot.register_next_step_handler(message, get_date)  

    
    if user_id in user_data:
        user_data.pop(user_id)

@bot.message_handler(commands=["list"])
def list_birthdays(message):
    user_id = str(message.chat.id)
    if user_id in birthdays and birthdays[user_id]:
        reply = "Your Saved Birthdays:\n\n" + "\n".join([f"{name}: {date}" for name, date in birthdays[user_id].items()])
    else:
        reply = "You have no saved birthdays."
    bot.send_message(message.chat.id, reply)

bot.infinity_polling()
