import os

import config
import workWithJSON as wJSON
import telebot
import keyboard as kb
import strings
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
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    global whichWayIs

    # Обработка ReplyKeyboardMarkup
    if message.text == strings.SEARCH_BY_GROUP:
        whichWayIs = 0
        howManyParameters[whichWayIs] = 0
        arrayGroup[0] = ''
        bot.send_message(message.chat.id, strings.ENTER_GROUP)
    elif message.text == strings.SEARCH_BY_SUBGROUP:
        whichWayIs = 1
        bot.send_message(message.chat.id, strings.ENTER_SUBGROUP)
    elif message.text == strings.SEARCH_BY_TEACHER:
        whichWayIs = 2
        howManyParameters[whichWayIs] = 0
        arrayTeacher[0] = ''
        bot.send_message(message.chat.id, strings.ENTER_TEACHER)
    elif message.text == strings.SEARCH_ALL_TIME_TABLE:
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
                bot.send_message(message.chat.id, strings.ENTER_DATE)
            elif not message.text == strings.SEARCH_BY_GROUP:
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_GROUP)

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
                bot.send_message(message.chat.id, strings.ENTER_DATE)
            elif not message.text == strings.SEARCH_BY_TEACHER:
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_TEACHER)

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
                teacher = wJSON.search_by_teacher_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
                bot.send_message(message.chat.id, teacher)


    elif whichWayIs == 3:
        print('4')
        if howManyParameters[whichWayIs] == 0:
            bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                             reply_markup=kb.choiceCourse)
            howManyParameters[whichWayIs] += 1
        elif howManyParameters[whichWayIs] == 1:
            if message.text == 'все':
                bot.send_message(message.chat.id, wJSON.print_all_time_table())
            elif message.text == 'выйти':
                howManyParameters[whichWayIs] = 0
                whichWayIs = -1
                bot.send_message(message.chat.id,
                                 message.from_user.username + ' выберите:',
                                 reply_markup=kb.choiceMarkup)
            else:
                year = str(int(message.text) % 100)
                bot.send_message(message.chat.id, wJSON.print_all_time_table_with_course(year))


if __name__ == '__main__':
    bot.polling(none_stop=True)
