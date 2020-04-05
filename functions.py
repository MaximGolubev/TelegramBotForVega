import workWithJSON as wJSON
import keyboard as kb
import strings
import main

import datetime
from telebot.types import Message

whichWayIs = -1
howManyParameters = [0, 0, 0, 0]
arrayGroup = ['']
arraySmallGroup = []
arrayTeacher = ['']
arrayAllTimeTable = ['']


def general_func(message: Message):
    # Обработка выбора пути с ReplyKeyboardMarkup
    str = choose_way(message)
    if not str == '':
        main.bot.send_message(message.chat.id, str)

    # Работа с выводом информации--------------
    if whichWayIs == 0:
        print('1')
        if howManyParameters[whichWayIs] == 0:
            stringOut = group_zero_parameters(message)
            if not stringOut == '':
                main.bot.send_message(message.chat.id, stringOut)
        elif howManyParameters[whichWayIs] == 1:
            stringOut = group_one_parameter(message)
            main.bot.send_message(message.chat.id, stringOut)

    elif whichWayIs == 1:
        print('2')

    elif whichWayIs == 2:
        print('3')
        if howManyParameters[whichWayIs] == 0:
            stringOut = teacher_zero_parameters(message)
            if not stringOut == '':
                main.bot.send_message(message.chat.id, stringOut)
        elif howManyParameters[whichWayIs] == 1:
            stringOut = teacher_one_parameter(message)
            main.bot.send_message(message.chat.id, stringOut)

    elif whichWayIs == 3:
        print('4')
        if howManyParameters[whichWayIs] == 0:
            main.bot.send_message(message.chat.id, strings.ENTER_COURSE_YEAR,
                                  reply_markup=kb.choiceCourse)
            howManyParameters[whichWayIs] += 1
        elif howManyParameters[whichWayIs] == 1:
            strOut = all_time_table_one_parameters(message)
            if message.text == 'выйти':
                main.bot.send_message(message.chat.id,
                                      message.from_user.username + ' выберите:',
                                      reply_markup=kb.choiceMarkup)
            else:
                main.bot.send_message(message.chat.id, strOut)


def choose_way(message: Message):
    global whichWayIs
    if message.text == strings.SEARCH_BY_GROUP:
        whichWayIs = 0
        howManyParameters[whichWayIs] = 0
        arrayGroup[0] = ''
        # bot.send_message(message.chat.id, strings.ENTER_GROUP)
        return strings.ENTER_GROUP
    elif message.text == strings.SEARCH_BY_SUBGROUP:
        whichWayIs = 1
        # bot.send_message(message.chat.id, strings.ENTER_SUBGROUP)
        return strings.ENTER_SUBGROUP
    elif message.text == strings.SEARCH_BY_TEACHER:
        whichWayIs = 2
        howManyParameters[whichWayIs] = 0
        arrayTeacher[0] = ''
        # bot.send_message(message.chat.id, strings.ENTER_TEACHER)
        return strings.ENTER_TEACHER
    elif message.text == strings.SEARCH_ALL_TIME_TABLE:
        whichWayIs = 3
        howManyParameters[whichWayIs] = 0
        arrayAllTimeTable[0] = ''
        return ''
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
            arrayData = message.text.split('.')
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
        arrayData = message.text.split('.')
        date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
        teacher = wJSON.search_by_teacher_and_date(arrayTeacher[0], wJSON.week_to_string(date.weekday()))
        # bot.send_message(message.chat.id, teacher)
        return teacher


def all_time_table_one_parameters(message: Message):
    global whichWayIs
    if message.text == 'все':
        # bot.send_message(message.chat.id, wJSON.print_all_time_table())
        return wJSON.print_all_time_table()
    elif message.text == 'выйти':
        howManyParameters[whichWayIs] = 0
        whichWayIs = -1
    else:
        year = str(int(message.text) % 100)
        # bot.send_message(message.chat.id, wJSON.print_all_time_table_with_course(year))
        return wJSON.print_all_time_table_with_course(year)
