import workWithJSON as wJSON
import functions as f

import re
import datetime
from telebot import types


def general_func(query):
    textIn = query.query
    digits_pattern = re.compile(r'[A-Za-zА-Яа-яёЁ]$', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, textIn)
    except AttributeError as ex:
        return 'ERROR'

    arrayCommands = textIn.upper().split(' ')
    l = len(arrayCommands)

    a = []

    try:
        if l == 1:
            a = len_one(arrayCommands)
        elif l == 2:
            a = len_two(arrayCommands)
        elif l == 3:
            a = len_three(arrayCommands)
        elif l == 4:
            a = len_four(arrayCommands)
    except:
        return a
    return a


def len_one(arrayCommands):
    if len(arrayCommands[0]) == 4:
        arrayGroupsOut = []
        if 'КММО' == arrayCommands[0][0:4] or 'КМБО' == arrayCommands[0][0:4]:
            print('query: ' + '1 - по группе')
            arrayGroupsIn = wJSON.search_group_by_one_part(arrayCommands[0])
            for i in range(0, len(arrayGroupsIn)):
                date = datetime.datetime.today()
                strOut = wJSON.search_by_group_and_date(arrayGroupsIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i+1), title=arrayGroupsIn[i],
                    description='Расписание на текущий день.',
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayGroupsOut.append(out)
        return arrayGroupsOut
    else:
        arrayTeachersIn = wJSON.search_teacher(arrayCommands[0])
        l = len(arrayTeachersIn)
        arrayTeachersOut = []
        if l > 0:
            print('query: ' + '1 - по преподавателю')
            for i in range(0, l):
                date = datetime.datetime.today()
                strOut = wJSON.search_by_teacher_and_date(arrayTeachersIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i + 1), title=arrayTeachersIn[i],
                    description='Расписание на текущий день.',
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayTeachersOut.append(out)
        return arrayTeachersOut


def len_two(arrayCommands):
    if len(arrayCommands[0]) == 4:
        arrayGroupsOut = []
        if 'КММО' == arrayCommands[0][0:4] or 'КМБО' == arrayCommands[0][0:4]:
            print('query: ' + '2 - по группе')
            arrayGroupsIn = wJSON.search_group_by_two_parts(arrayCommands[0], arrayCommands[1])
            for i in range(0, len(arrayGroupsIn)):
                date = datetime.datetime.today()
                strOut = wJSON.search_by_group_and_date(arrayGroupsIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i+1), title=arrayGroupsIn[i],
                    description='Расписание на текущий день.',
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayGroupsOut.append(out)
        return arrayGroupsOut

    else:
        arrayTeachersIn = wJSON.search_teacher(arrayCommands[0])
        l = len(arrayTeachersIn)
        arrayTeachersOut = []
        if l > 0:
            print('query: ' + '2 - по преподавателю')
            try:
                arrayData = f.data_to_array(arrayCommands[1])
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
            except:
                return arrayTeachersOut
            for i in range(0, l):
                strOut = wJSON.search_by_teacher_and_date(arrayTeachersIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i + 1), title=arrayTeachersIn[i],
                    description='Расписание на: '
                                + arrayData[0] + '.'
                                + arrayData[1] + '.'
                                + arrayData[2] + ' - '
                                + wJSON.week_to_string(date.weekday()),
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayTeachersOut.append(out)
        return arrayTeachersOut


def len_three(arrayCommands):
    if len(arrayCommands[0]) == 4:
        arrayGroupsOut = []
        if 'КММО' == arrayCommands[0][0:4] or 'КМБО' == arrayCommands[0][0:4]:
            print('query: ' + '3 - по группе')
            arrayGroupsIn = wJSON.search_group_by_three_parts(arrayCommands[0], arrayCommands[1], arrayCommands[2])
            for i in range(0, len(arrayGroupsIn)):
                date = datetime.datetime.today()
                strOut = wJSON.search_by_group_and_date(arrayGroupsIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i+1), title=arrayGroupsIn[i],
                    description='Расписание на текущий день.',
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayGroupsOut.append(out)
        return arrayGroupsOut

def len_four(arrayCommands):
    if len(arrayCommands[0]) == 4:
        arrayGroupsOut = []
        if 'КММО' == arrayCommands[0][0:4] or 'КМБО' == arrayCommands[0][0:4]:
            print('query: ' + '4 - по группе')
            arrayGroupsIn = wJSON.search_group_by_three_parts(arrayCommands[0], arrayCommands[1], arrayCommands[2])
            for i in range(0, len(arrayGroupsIn)):
                try:
                    arrayData = f.data_to_array(arrayCommands[3])
                    date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                except:
                    return arrayGroupsOut
                strOut = wJSON.search_by_group_and_date(arrayGroupsIn[i], wJSON.week_to_string(date.weekday()))
                out = types.InlineQueryResultArticle(
                    id=str(i+1), title=arrayGroupsIn[i],
                    description='Расписание на: '
                                + arrayData[0] + '.'
                                + arrayData[1] + '.'
                                + arrayData[2] + ' - '
                                + wJSON.week_to_string(date.weekday()),
                    input_message_content=types.InputTextMessageContent(message_text=strOut))
                arrayGroupsOut.append(out)
        return arrayGroupsOut
