import config
import functions as f
import strings
import keyboard as kb
import workWithDataBase as wDB

import os
import telebot
from telebot.types import Message

# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token
USERDIRECTORY = os.getcwd()

bot = telebot.TeleBot(TOKEN)

wDB.init_data_base()


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.from_user.id, 'Привет, '
                     + message.from_user.username + '!\nВыберите:',
                     reply_markup=kb.choiceMarkup)
    wDB.add_user(chat_id=message.chat.id)
    print(message.chat.id)
    print('/start')


@bot.message_handler(commands=['setnew'])
def time_table_changed(message: Message):
    if (f.isAdmin(message.chat.id)):
        str = message.text.split(' ')
        option = ''
        if len(str) > 1:
            for i in range(1, len(str)):
                option += str[i] + ' '
        f.sendNotif(option)
        print(message.chat.id)
        print('/setnew ' + option)
    else:
        print("----- ВНИМАНИЕ!!! "
              "\n----- пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал 'setnew'"
              "\n----- chat_id: " + str(message.chat.id)
              + "\n----- username: " + str(message.from_user.username))


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)
    print(message.chat.id)
    print('/help')


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    wDB.add_user(chat_id=message.chat.id)
    f.general_func(message)
    print(message.chat.id)
    print('/text')
    print("'" + message.text + "'")


if __name__ == '__main__':
    bot.polling(none_stop=True)
