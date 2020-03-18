import os
import config
import workWithJSON as wJSON
import telebot
from telebot.types import Message
# from telebot import apihelper

# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token
# PROXY = os.environ.get('PROXY_FOR_VEGA_BOT')
USERDIRECTORY = os.getcwd()

bot = telebot.TeleBot(TOKEN)
path_saved_files = "/".join(("SavedInformation", "SavedFiles"))
path_saved_photos = "/".join(("SavedInformation", "SavedPhotos"))
# apihelper.proxy = {'https': PROXY}

if not os.path.exists("SavedInformation"):
    os.mkdir("SavedInformation")
    os.mkdir(path_saved_files)
    os.mkdir(path_saved_photos)


@bot.message_handler(commands=['start'])
def send_welcome(message: Message):
    bot.send_message(message.chat.id, "Привет, " + message.from_user.username
                                        + "!\nВыберите: (цифру) "
                                        "\n1 - Поиск по группе "
                                        "\n2 - Поиск преподавателя "
                                        "\n3 - Вывод полного расписания")


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    bot.send_message(message.chat.id, "help - дерево параметров поиска\n"
                     "Дерево поиска:\n" +
                     "1) Поиск по группе - название группы - "
                     "день недели (необязательно)\n" +
                     "2) Поиск преподавателя - фамилия преподавателя - "
                     "день недели (необязательно)\n" +
                     "3) Вывод полного расписания - номер курса (необязательно)")


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    group = wJSON.search_by_group(message.text)
    if group == 'Error!':
        bot.send_message(message.chat.id, 'Ошибка! Групп с названием: ' + message.text + ' нет')
    else:
        bot.send_message(message.chat.id, group)


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
