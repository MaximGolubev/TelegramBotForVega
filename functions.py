import workWithJSON as wJSON
import keyboard as kb
import main
from main import dataBase
import strings
import config

import time
import datetime
import telebot
from telebot.types import Message

bot = telebot.TeleBot(config.token)

# whichWayIs - это состояние, в котором мы находимся?
# если да, эта штука не будет работать при одновременной работе нескольких юзеров
# (будут воровать друг у друга состояние)
# Надо сохранять состояние в словаре или БД (vedis, redis)
#way = -1
#countParam = 0
#arrayGroup = ['']
#arrayTeacher = ['']

fileProvider = wJSON.FileProvider("dataTest.json")
jsonFormatter = wJSON.JsonFormatter(fileProvider)

def general_func(message: Message):
    # Обработка выбора пути с ReplyKeyboardMarkup
    s = choose_way(message)
    if not s == '':
        bot.send_message(message.chat.id, s)
    row = dataBase.get_row_by_id(message.from_user.id)
    list = row_to_list(row)
    way = row[3]
    countParam = row[4]
    # Работа с выводом информации--------------
    if way == 0:
        if countParam == 0:
            stringOut = group_zero_parameters(message)
            if not stringOut == '':
                bot.send_message(message.chat.id, stringOut)
        elif countParam == 1:
            stringOut = group_one_parameter(message)
            bot.send_message(message.chat.id, stringOut)


    elif way == 1:
        if countParam == 0:
            stringOut = teacher_zero_parameters(message)
            if not stringOut == '':
                bot.send_message(message.chat.id, stringOut)
        elif countParam == 1:
            stringOut = teacher_one_parameter(message)
            bot.send_message(message.chat.id, stringOut)


    elif way == 2:
        if countParam == 0:
            list[4] += 1
            bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                             reply_markup=kb.choiceCourse)
            dataBase.edit_row(list[0], list)
        elif countParam == 1:
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
                main.loggerDEBUG.debug('вывод всего расписания (null)')
                bot.send_message(message.chat.id, strings.MESSAGE_ERROR_ALL_TIME_TABLE)

    elif way == 3:
        main.loggerDEBUG.debug('когда свободна Б-209? (0)')
        bot.send_message(message.chat.id, jsonFormatter.when_b209_is_free())
        list[3] = -1
        dataBase.edit_row(list[0], list)

# разбить на отдельные хендлеры: код будет прозрачнее
def choose_way(message: Message):
    row = dataBase.get_row_by_id(message.from_user.id)
    if row == 'ERROR':
        return 1
    buf_list = row_to_list(row)

    if message.text == strings.SEARCH_BY_GROUP:
        main.loggerDEBUG.debug('поиск по группе')
        buf_list[3] = 0
        buf_list[4] = 0
        buf_list[5] = ''
        dataBase.edit_row(buf_list[0], buf_list)
        # bot.send_message(message.chat.id, strings.ENTER_GROUP)
        return strings.ENTER_GROUP
    elif message.text == strings.SEARCH_BY_TEACHER:
        main.loggerDEBUG.debug('поиск по преподавателю')
        buf_list[3] = 1
        buf_list[4] = 0
        buf_list[6] = ''
        dataBase.edit_row(buf_list[0], buf_list)
        # bot.send_message(message.chat.id, strings.ENTER_TEACHER)
        return strings.ENTER_TEACHER
    elif message.text == strings.SEARCH_ALL_TIME_TABLE:
        main.loggerDEBUG.debug('вывод всего расписания')
        buf_list[3] = 2
        buf_list[4] = 0
        dataBase.edit_row(buf_list[0], buf_list)
        return ''
    elif message.text == strings.SEARCH_BY_B209:
        main.loggerDEBUG.debug('когда свободна Б209?')
        buf_list[3] = 3
        buf_list[4] = 0
        dataBase.edit_row(buf_list[0], buf_list)
        # bot.send_message(message.chat.id, strings.ENTER_SUBGROUP)
        return strings.ENTER_SUBGROUP
    else:
        return ''


def group_zero_parameters(message: Message):
    main.loggerDEBUG.debug('поиск по группе (0)')
    row = dataBase.get_row_by_id(message.from_user.id)
    list = row_to_list(row)

    gr = fileProvider.search_group(message.text)
    if not gr == 'ERROR':
        list[5] = message.text.upper()
        list[4] += 1
        dataBase.edit_row(list[0], list)
        # bot.send_message(message.chat.id, strings.ENTER_DATE)
        return strings.ENTER_DATE
    elif not message.text == strings.SEARCH_BY_GROUP:
        # bot.send_message(message.chat.id, strings.MESSAGE_ERROR_GROUP)
        return strings.MESSAGE_ERROR_GROUP
    else:
        return ''

# разбить на отдельные хендлеры: код будет прозрачнее
def group_one_parameter(message: Message):
    main.loggerDEBUG.debug('поиск по группе (1)')
    row = dataBase.get_row_by_id(message.from_user.id)
    list = row_to_list(row)
    if message.text == '1':
        date = datetime.datetime.today()
        group = jsonFormatter.search_by_group_and_date(list[5], wJSON.week_to_string(date.weekday()))
        # bot.send_message(message.chat.id, group)
        return group
    elif message.text == '7':
        group = jsonFormatter.search_by_group(list[5])
        # bot.send_message(message.chat.id, group)
        return group
    else:
        try:
            # arrayData = message.text.split('.')
            arrayData = data_to_array(message.text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            group = jsonFormatter.search_by_group_and_date(list[5], wJSON.week_to_string(date.weekday()))
            return group
        except:
            return 'Некорректный ввод даты.\n' \
                   'Повторите снова.'


def teacher_zero_parameters(message: Message):
    main.loggerDEBUG.debug('поиск по преподавателю (0)')
    row = dataBase.get_row_by_id(message.from_user.id)
    list = row_to_list(row)
    tch = fileProvider.search_subject(message.text)
    if not tch == 'ERROR':
        list[6] = message.text.upper()
        list[4] += 1
        dataBase.edit_row(list[0], list)
        # bot.send_message(message.chat.id, strings.ENTER_DATE)
        return strings.ENTER_DATE
    elif not message.text == strings.SEARCH_BY_TEACHER:
        # bot.send_message(message.chat.id, strings.MESSAGE_ERROR_TEACHER)
        return strings.MESSAGE_ERROR_TEACHER
    else:
        return ''


def teacher_one_parameter(message: Message):
    main.loggerDEBUG.debug('поиск по преподавателю (1)')
    row = dataBase.get_row_by_id(message.from_user.id)
    list = row_to_list(row)
    if message.text == '1':
        date = datetime.datetime.today()
        teacher = jsonFormatter.search_by_teacher_and_date(list[6], wJSON.week_to_string(date.weekday()))
        # bot.send_message(message.chat.id, teacher)
        return teacher
    elif message.text == '7':
        teacher = jsonFormatter.search_by_teacher(list[6])
        # bot.send_message(message.chat.id, teacher)
        return teacher
    else:
        try:
            arrayData = data_to_array(message.text)
            date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            teacher = jsonFormatter.search_by_teacher_and_date(list[6], wJSON.week_to_string(date.weekday()))
            # bot.send_message(message.chat.id, teacher)
            return teacher
        except:
            return 'Некорректный ввод даты.\n' \
                   'Повторите снова.'


def all_time_table_one_parameters(message: Message):
    main.loggerDEBUG.debug('вывод всего расписания (0)')
    row = dataBase.get_row_by_id(message.from_user.id)
    buf_list = row_to_list(row)
    # print ("-------------")
    if message.text == 'все':
        # print("-------------")
        # bot.send_message(message.chat.id, wJSON.print_all_time_table())
        s = jsonFormatter.print_all_time_table()
        return s
    elif message.text == 'выйти':
        buf_list[4] = 0
        buf_list[3] = -1
        dataBase.edit_row(buf_list[0], buf_list)
    else:
        year = f'{(int(message.text[2:4]) % 100)}'
        strGroup = ''
        if message.text[4:] == ' (магистратура)':
            strGroup += 'КММО'
        elif message.text[4:] == ' (бакалавриат)':
            strGroup += 'КМБО'
        else:
            return 'ERROR'
        # bot.send_message(message.chat.id, wJSON.print_all_time_table_with_course(year))
        return jsonFormatter.print_all_time_table_with_course(strGroup, year)


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
    pass
    # connection = dataBase.get_user_connection()
    # db = connection.cursor()
    # db.execute("SELECT * FROM all_users")
    # timing = time.time()
    # while True:
    #     if time.time() - timing > 0.05:
    #         timing = time.time()
    #         row = db.fetchone()
    #         if row == None:
    #             break
    #
    #         chat_id = row[2]
    #         try:
    #             db.close()
    #             bot.send_message(chat_id, strings.MESSAGE_SEND_NOTIFICATION_first + s + strings.MESSAGE_SEND_NOTIFICATION_second)
    #         except:
    #             db.close()
    #             main.loggerDEBUG.warning(f'----- в chat_id: {chat_id} уведомление отправлено не было')
    #

def isAdmin(id):
    pass
    # connection = dataBase.get_admin_connection()
    # db = connection.cursor()
    # db.execute("SELECT * FROM admins")
    # while True:
    #     row = db.fetchone()
    #     if row == None:
    #         break
    #
    #     user_id = row[1]
    #     if int(user_id) == int(id):
    #         db.close()
    #         return True
    # db.close()
    # return False


def row_to_list(row):
    print(row)
    buf_list = [row[0], row[1], row[2], row[3], row[4], row[5], row[6]]
    return buf_list
