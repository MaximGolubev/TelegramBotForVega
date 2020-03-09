from telebot.types import Message
#from telebot import apihelper
import config
import telebot
import os

BOT = telebot.TeleBot(config.token)
TOKEN = config.token
USERDIRECTORY = os.getcwd()
#PROXY =

path_saved_files = f'{USERDIRECTORY}\\SavedInformation\\SavedFiles'
path_saved_photos = f'{USERDIRECTORY}\\SavedInformation\\SavedPhotos'
#apihelper.proxy = {'https': PROXY}

if not os.path.exists("SavedInformation"):
    os.mkdir("SavedInformation")
    os.mkdir(path_saved_files)
    os.mkdir(path_saved_photos)


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    BOT.send_message(message.chat.id,
                     "Hello, " + message.from_user.first_name + " " + message.from_user.last_name + "!")


@BOT.message_handler(commands=['help'])
def send_welcome(message: Message):
    BOT.send_message(message.chat.id, "start - начало беседы с ботом\nhelp - полный список команд\nspecialInformation "
                                      "- дополнительная информация")
    #BOT.send_message(message.chat.id, "Директория:\n" + USERDIRECTORY)


@BOT.message_handler(commands=['specialInformation'])
def send_special_inf(message):
    BOT.send_message(message.chat.id, "Ваш логин: " + str(message.from_user.username) + "\nВаш Id: " + str(
        message.from_user.id) + "\nId чата: " + str(message.chat.id))


@BOT.message_handler(func=lambda message: True)
def repeat_all_messages(message: Message):
    BOT.send_message(message.chat.id, message.text)


@BOT.message_handler(content_types=['document'])
def repeat_all_messages(message: Message):

    try:
        file_info = BOT.get_file(message.document.file_id)
        downloaded_file = BOT.download_file(file_info.file_path)

        src = path_saved_files + "/" + message.document.file_name
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        BOT.send_message(message.chat.id, "Сохранение выполнено успешно")

        document = open(src, 'rb')
        BOT.send_document(message.chat.id, document)

    except Exception as e:
        BOT.reply_to(message, e)


@BOT.message_handler(content_types=['photo'])
def repeat_all_messages(message: Message):

    try:
        file_info = BOT.get_file(message.photo[0].file_id)
        downloaded_file = BOT.download_file(file_info.file_path)

        src = path_saved_photos + "/" + message.photo[0].file_id
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        BOT.send_message(message.chat.id, "Сохранение выполнено успешно")

        img = open(src, 'rb')
        BOT.send_photo(message.chat.id, img)

    except Exception as e:
        BOT.reply_to(message, e)


if __name__ == '__main__':
    BOT.polling(none_stop=True)
