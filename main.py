from telebot.types import Message
#from telebot import apihelper
import config
import telebot
import os


TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
#PROXY = os.environ.get('PROXY_FOR_VEGA_BOT')
USERDIRECTORY = os.getcwd()

bot = telebot.TeleBot(TOKEN)
path_saved_files = "/".join(("SavedInformation", "SavedFiles"))
path_saved_photos = "/".join(("SavedInformation", "SavedPhotos"))
#apihelper.proxy = {'https': PROXY}

if not os.path.exists("SavedInformation"):
    os.mkdir("SavedInformation")
    os.mkdir(path_saved_files)
    os.mkdir(path_saved_photos)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Hello, " + message.from_user.username + "!")


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    bot.send_message(message.chat.id, "start - начало беседы с ботом\n" +
                     "help - полный список команд\n"
                     "specialInformation " + "- дополнительная информация")


@bot.message_handler(commands=['specialInformation'])
def send_special_inf(message):
    bot.send_message(message.chat.id,
                     "Ваш логин: " + str(message.from_user.username) +
                     "\nВаш Id: " + str(message.from_user.id) +
                     "\nId чата: " + str(message.chat.id))


@bot.message_handler(func=lambda message: True)
def repeat_message(message: Message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(content_types=['document'])
def save_and_send_document(message: Message):

    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "/".join((path_saved_files, message.document.file_name))
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        bot.send_message(message.chat.id, "Сохранение выполнено успешно")

        document = open(src, 'rb')
        bot.send_document(message.chat.id, document)

    except Exception as e:
        bot.reply_to(message, e)


@bot.message_handler(content_types=['photo'])
def save_and_send_photo(message: Message):

    try:
        file_info = bot.get_file(message.photo[0].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        src = "/".join((path_saved_photos, message.photo[0].file_id))
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
            new_file.close()

        bot.send_message(message.chat.id, "Сохранение выполнено успешно")

        img = open(src, 'rb')
        bot.send_photo(message.chat.id, img)

    except Exception as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    bot.polling(none_stop=True)
