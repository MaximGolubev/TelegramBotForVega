import time

import workWithJSON as wJSON
import workWithDataBase as wDB
import keyboard as kb
import strings
import config

import datetime
import telebot
from telebot.types import Message

bot = telebot.TeleBot(config.token)

# whichWayIs - это состояние, в котором мы находимся?
# если да, эта штука не будет работать при одновременной работе нескольких юзеров
# (будут воровать друг у друга состояние)
# Надо сохранять состояние в словаре или БД (vedis, redis)
whichWayIs = -1
howManyParameters = [0, 0, 0, 0]
arrayGroup = ['']
arraySmallGroup = []
arrayTeacher = ['']
arrayAllTimeTable = ['']


def general_func(message: Message):
    # Обработка выбора пути с ReplyKeyboardMarkup
    global whichWayIs
    str = choose_way(message) # str это тип, переименовать
    if not str == '':
        bot.send_message(message.chat.id, str)

    # Работа с выводом информации--------------
    if whichWayIs == 0:
        print('+ in bot: ' + 'Поиск по группе')
        if howManyParameters[whichWayIs] == 0:
            stringOut = group_zero_parameters(message)
            if not stringOut == '':
                bot.send_message(message.chat.id, stringOut)
        elif howManyParameters[whichWayIs] == 1:
            stringOut = group_one_parameter(message)
            bot.send_message(message.chat.id, stringOut)


    elif whichWayIs == 1:
        print('+ in bot: ' + 'Поиск по преподавателю')
        if howManyParameters[whichWayIs] == 0:
            stringOut = teacher_zero_parameters(message)
            if not stringOut == '':
                bot.send_message(message.chat.id, stringOut)
        elif howManyParameters[whichWayIs] == 1:
            stringOut = teacher_one_parameter(message)
            bot.send_message(message.chat.id, stringOut)


    elif whichWayIs == 2:
        print('+ in bot: ' + 'Вывод всего расписания')
        if howManyParameters[whichWayIs] == 0:
            bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                             reply_markup=kb.choiceCourse)
            howManyParameters[whichWayIs] += 1
        elif howManyParameters[whichWayIs] == 1:
            catch = catching_stupid_in_third(message.text)
            if not catch:
                strOut = all_time_table_one_parameters(message)
                if message.text == 'выйти':
                    bot.send_message(message.chat.id,
                                     message.from_user.username + ' выберите:',
                                     reply_markup=kb.choiceMarkup)
                else:
                    l = len(strOut)
                    # print(l)
                    if l == 6:
                        for i in range(0, l):
                            # print(strOut[i] + "=========================================================================")
                            if not strOut[i] == '':
                                bot.send_message(message.chat.id, strOut[i])
                    else:
                        bot.send_message(message.chat.id, strOut)
            else:
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_ALL_TIME_TABLE)

    elif whichWayIs == 3:
        print('+ in bot: ' + 'Когда свободна Б-209?')
        bot.send_message(message.chat.id, wJSON.when_b209_is_free())
        whichWayIs = -1

# разбить на отдельные хендлеры: код будет прозрачнее
def choose_way(message: Message):
    global whichWayIs
    if message.text == strings.SEARCH_BY_GROUP:
        whichWayIs = 0
        howManyParameters[whichWayIs] = 0
        arrayGroup[0] = ''
        # bot.send_message(message.chat.id, strings.ENTER_GROUP)
        return strings.ENTER_GROUP
    elif message.text == strings.SEARCH_BY_TEACHER:
        whichWayIs = 1
        howManyParameters[whichWayIs] = 0
        arrayTeacher[0] = ''
        # bot.send_message(message.chat.id, strings.ENTER_TEACHER)
        return strings.ENTER_TEACHER
    elif message.text == strings.SEARCH_ALL_TIME_TABLE:
        whichWayIs = 2
        howManyParameters[whichWayIs] = 0
        arrayAllTimeTable[0] = ''
        return ''
    elif message.text == strings.SEARCH_BY_B209:
        whichWayIs = 3
        # bot.send_message(message.chat.id, strings.ENTER_SUBGROUP)
        return strings.ENTER_SUBGROUP
    else:
        return ''


def group_zero_parameters(message: Message):
    gr = wJSON.search_group(message.text)
    if not gr == 'ERROR':
        arrayGroup[0] = message.text.upper()
        howManyParameters[whichWayIs] += 1
        # bot.send_message(message.chat.id, strings.ENTER_DATE)
        return strings.ENTER_DATE
    elif not message.text == strings.SEARCH_BY_GROUP:
        # bot.send_message(message.chat.id, strings.MESSAGE_ERROR_GROUP)
        return strings.MESSAGE_ERROR_GROUP
    else:
        return ''

# разбить на отдельные хендлеры: код будет прозрачнее
def group_one_parameter(message: Message):
    if message.text == '1':
        date = datetime.datetime.today()
        group = wJSON.search_by_group_and_date(arrayGroup[0], wJSON.week_to_string(date.weekday()))
        # bot.send_message(message.chat.id, group)
        return group
    elif message.text == '7':
        group = wJSON.search_by_group(arrayGroup[0])
        # bot.send_message(message.chat.id, group)
        return group
    else:
        try:
            # arrayData = message.text.split('.')
            arrayData = data_to_array(message.text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            group = wJSON.search_by_group_and_date(arrayGroup[0], wJSON.week_to_string(date.weekday()))
            return group
        except:
            return 'Некорректный ввод даты.\n' \
                   'Повторите снова.'


def teacher_zero_parameters(message: Message):
    tch = wJSON.search_subject(message.text)
    if not tch == 'ERROR':
        arrayTeacher[0] = message.text.upper()
        howManyParameters[whichWayIs] += 1
        # bot.send_message(message.chat.id, strings.ENTER_DATE)
        return strings.ENTER_DATE
    elif not message.text == strings.SEARCH_BY_TEACHER:
        # bot.send_message(message.chat.id, strings.MESSAGE_ERROR_TEACHER)
        return strings.MESSAGE_ERROR_TEACHER
    else:
        return ''


def teacher_one_parameter(message: Message):
    if message.text == '1':
        date = datetime.datetime.today()
        teacher = wJSON.search_by_teacher_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
        # bot.send_message(message.chat.id, teacher)
        return teacher
    elif message.text == '7':
        teacher = wJSON.search_by_teacher(arrayTeacher[0])
        # bot.send_message(message.chat.id, teacher)
        return teacher
    else:
        try:
            arrayData = data_to_array(message.text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            teacher = wJSON.search_by_teacher_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
            # bot.send_message(message.chat.id, teacher)
            return teacher
        except:
            return 'Некорректный ввод даты.\n' \
                   'Повторите снова.'


def all_time_table_one_parameters(message: Message):
    global whichWayIs
    # print ("-------------")
    if message.text == 'все':
        # print("-------------")
        # bot.send_message(message.chat.id, wJSON.print_all_time_table())
        s = wJSON.print_all_time_table()
        return s
    elif message.text == 'выйти':
        howManyParameters[whichWayIs] = 0
        whichWayIs = -1
    else:
        year = str(int(message.text[2:4]) % 100)
        strGroup = ''
        if message.text[4:] == ' (магистратура)':
            strGroup += 'КММО'
        elif message.text[4:] == ' (бакалавриат)':
            strGroup += 'КМБО'
        else:
            return 'ERROR'
        # bot.send_message(message.chat.id, wJSON.print_all_time_table_with_course(year))
        return wJSON.print_all_time_table_with_course(strGroup, year)


def catching_stupid_in_third(text):
    if text == kb.STRBUTTONSTHIRD_1:
        return False
    elif text == kb.STRBUTTONSTHIRD_2:
        return False
    elif text == kb.STRBUTTONSTHIRD_3:
        return False
    elif text == kb.STRBUTTONSTHIRD_4:
        return False
    elif text == kb.STRBUTTONSTHIRD_5:
        return False
    elif text == kb.STRBUTTONSTHIRD_6:
        return False
    elif text == kb.STRBUTTONSTHIRD_7:
        return False
    elif text == kb.STRBUTTONSTHIRD_8:
        return False
    return True


def data_to_array(strData):
    array = ['', '', '']
    l = len(strData)
    if l == 10:
        array[0] = strData[0:2]
        array[1] = strData[3:5]
        array[2] = strData[6:]
        if strData[2] != strData[5]:
            array = ['', '', '']
    elif l == 8:
        array[0] = strData[0:2]
        array[1] = strData[2:4]
        array[2] = strData[4:]

    if array[0] == '' or array[1] == '' or array[2] == '':
        return 'Некорректный ввод даты.\n' \
               'Повторите снова.'
    else:
        return array


def sendNotif(s):
    connection = wDB.get_connection_to_users_data_base()
    db = connection.cursor()
    db.execute("SELECT * FROM all_users_chat_id")
    timing = time.time()
    while True:
        if time.time() - timing > 0.05:
            timing = time.time()
            row = db.fetchone()
            if row == None:
                break

            chat_id = row[1]
            try:
                bot.send_message(chat_id, strings.MESSAGE_SEND_NOTIFICATION_first + s + strings.MESSAGE_SEND_NOTIFICATION_second)
            except:
                print("----- в chat_id:" + str(chat_id) + " уведомление отправлено не было")


def isAdmin(id):
    connection = wDB.get_connection_to_admin_data_base()
    db = connection.cursor()
    db.execute("SELECT * FROM admins_chat_id")
    while True:
        row = db.fetchone()
        if row == None:
            break

        chat_id = row[1]
        if int(chat_id) == int(id):
            return True
    return False
