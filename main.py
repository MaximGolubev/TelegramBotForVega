import os

import config
import workWithJSON as wJSON
import telebot
import keyboard as kb
import datetime
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

whichWayIs = -1
howManyParameters = [0, 0, 0, 0]
arrayGroup = ['']
arraySmallGroup = []
arrayTeacher = ['']
arrayAllTimeTable = ['']


if not os.path.exists("SavedInformation"):
    os.mkdir("SavedInformation")
    os.mkdir(path_saved_files)
    os.mkdir(path_saved_photos)


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    bot.send_message(message.from_user.id, 'Привет, '
                     + message.from_user.username + '!\nВыберите:',
                     reply_markup=kb.choiceMarkup)



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
    global whichWayIs

    # Обработка ReplyKeyboardMarkup
    if message.text == 'Поиск по группе':
        whichWayIs = 0
        howManyParameters[whichWayIs] = 0
        arrayGroup[0] = ''
        bot.send_message(message.chat.id, "Введите номер группы.\n(Пример: кмбо-04-20)")
    elif message.text == 'Поиск по подгруппе':
        whichWayIs = 1
        bot.send_message(message.chat.id, "Введите номер подгруппы.\n(Пример: 1)")
    elif message.text == 'Поиск по преподавателю':
        whichWayIs = 2
        howManyParameters[whichWayIs] = 0
        arrayTeacher[0] = ''
        bot.send_message(message.chat.id, "Введите фамилию преподавателя.\n(Пример: головин)")
    elif message.text == 'Вывод полного расписания':
        whichWayIs = 3
        howManyParameters[whichWayIs] = 0
        arrayAllTimeTable[0] = ''

    # Работа с выводом информации--------------
    if whichWayIs == 0:
        print('1')
        if howManyParameters[whichWayIs] == 0:
            gr = wJSON.search_group(message.text)
            if not gr == 'ERROR':
                arrayGroup[0] = message.text.upper()
                howManyParameters[whichWayIs] += 1
                bot.send_message(message.chat.id,
                                 "Введите дату в формате из примера "
                                 "или воспользуйтесь ключами:\n"
                                 "'1' (значение текущей даты)\n"
                                 "'7' (вывод расписания на целую неделю)\n"
                                 "ПРИМЕРЫ:\n21.08.2001\n1")
            elif not message.text == 'Поиск по группе':
                bot.send_message(message.chat.id, "Такой группы не существует.")

        elif howManyParameters[whichWayIs] == 1:
            if message.text == '1':
                date = datetime.datetime.today()
                group = wJSON.search_by_group_and_date(arrayGroup[0], wJSON.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, group)
            elif message.text == '7':
                group = wJSON.search_by_group(arrayGroup[0])
                bot.send_message(message.chat.id, group)
            else:
                arrayData = message.text.split('.')
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                group = wJSON.search_by_group_and_date(arrayGroup[0], wJSON.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, group)


    elif whichWayIs == 1:
        print('2')


    elif whichWayIs == 2:
        print('3')
        if howManyParameters[whichWayIs] == 0:
            tch = wJSON.search_subject(message.text)
            if not tch == 'ERROR':
                arrayTeacher[0] = message.text.upper()
                howManyParameters[whichWayIs] += 1
                bot.send_message(message.chat.id,
                                 "Введите дату в формате из примера "
                                 "или воспользуйтесь ключами:\n"
                                 "'1' (значение текущей даты)\n"
                                 "'7' (вывод расписания на целую неделю)\n"
                                 "ПРИМЕРЫ:\n21.08.2001\n1")
            elif not message.text == 'Поиск по преподавателю':
                bot.send_message(message.chat.id, "Такой преподаватель у нас не работает(")

        elif howManyParameters[whichWayIs] == 1:
            if message.text == '1':
                date = datetime.datetime.today()
                teacher = wJSON.search_by_teacher_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, teacher)
            elif message.text == '7':
                teacher = wJSON.search_by_teacher(arrayTeacher[0])
                bot.send_message(message.chat.id, teacher)
            else:
                arrayData = message.text.split('.')
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                teacher = wJSON.search_by_group_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, teacher)


    elif whichWayIs == 3:
        print('4')
        if howManyParameters[whichWayIs] == 0:
            bot.send_message(message.chat.id, wJSON.print_all_time_table())
        #elif howManyParameters[whichWayIs] == 1:


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
