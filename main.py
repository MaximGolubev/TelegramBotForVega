import config
import keyboard as kb
import functions as f
import strings
import workWithDataBase as wDB

import os
import telebot
from telebot.types import Message


# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token
USERDIRECTORY = os.getcwd()

bot = telebot.TeleBot(TOKEN)
path_saved_files = "/".join(("SavedInformation", "SavedFiles"))
path_saved_photos = "/".join(("SavedInformation", "SavedPhotos"))

if not os.path.exists("SavedInformation"):
    os.mkdir("SavedInformation")
    os.mkdir(path_saved_files)
    os.mkdir(path_saved_photos)

wDB.init_data_base()


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.from_user.id, 'Привет, '
                     + message.from_user.username + '!\nВыберите:',
                     reply_markup=kb.choiceMarkup)
    wDB.add_user(chat_id=message.chat.id)


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    f.general_func(message)


if __name__ == '__main__':
    bot.polling(none_stop=True)
