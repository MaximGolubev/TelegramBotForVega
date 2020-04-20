import datetime
import types

import workWithJSON as wJSON
import functions as f
import re

strDescipt = ''
strMore = ''


def general_func(query):
    textIn = query.query
    digits_pattern = re.compile(r'[A-Za-zА-Яа-яёЁ]$', re.MULTILINE)
    try:
        matches = re.match(digits_pattern, textIn)
    except AttributeError as ex:
        return 'ERROR'

    arrayCommands = textIn.upper().split(' ')
    l = len(arrayCommands)

    if l == 0:
        return 'ERROR'

    if l == 1:
        try:
            a = len_one(arrayCommands)
        except:
            return 'ERROR'
        return a

    elif l == 2:
        try:
            a = len_two(arrayCommands)
        except:
            return 'ERROR'
        return a

    return 'ERROR'


def len_one(arrayCommands):
    global strDescipt
    global strMore
    if (arrayCommands[0][0:4] == 'КММО' or arrayCommands[0][0:4] == 'КМБО') and not wJSON.search_group(
            arrayCommands[0]) == 'ERROR':
        print('1 - по группе')
        strOut = wJSON.search_by_group(arrayCommands[0])
        if strOut == '':
            return 'ERROR'
        strDescipt = wJSON.text_to_group(arrayCommands[0])
        strMore = 'всё расписание'
        return strOut
    elif not wJSON.search_teacher(arrayCommands[0]) == 'ERROR':
        teacher = wJSON.search_teacher(arrayCommands[0])
        print('1 - по преподавателю')
        strOut = wJSON.search_by_teacher(arrayCommands[0])
        if strOut == '':
            return 'ERROR'
        strDescipt = teacher.upper()
        strMore = 'всё расписание'
        return strOut
    else:
        return 'ERROR'


def len_two(arrayCommands):
    global strDescipt
    global strMore
    if (arrayCommands[0][0:4] == 'КММО' or arrayCommands[0][0:4] == 'КМБО') \
            and not wJSON.search_group(arrayCommands[0]) == 'ERROR':
        print('2 - по группе')
        if arrayCommands[1] == '1':
            date = datetime.datetime.today()
            strOut = wJSON.search_by_group_and_date(arrayCommands[0], wJSON.week_to_string(date.weekday()))
            strMore = 'расписание на текущий день'
        elif arrayCommands[1] == '7':
            strOut = wJSON.search_by_group(arrayCommands[0])
            strMore = 'всё расписание'
        else:
            try:
                arrayData = f.data_to_array(arrayCommands[1])
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                strOut = wJSON.search_by_group_and_date(arrayCommands[0], wJSON.week_to_string(date.weekday()))
                strMore = 'расписание на: ' + arrayData[0] + '.' + arrayData[1] + '.' + arrayData[2]
            except:
                return 'ERROR'

        strDescipt = wJSON.text_to_group(arrayCommands[0])
        return strOut

    elif not wJSON.search_teacher(arrayCommands[0]) == 'ERROR':
        teacher = wJSON.search_teacher(arrayCommands[0])
        print('2 - по преподавателю')
        if arrayCommands[1] == '1':
            date = datetime.datetime.today()
            strOut = wJSON.search_by_teacher_and_date(arrayCommands[0], wJSON.week_to_string(date.weekday()))
            strMore = 'расписание на текущий день'
        elif arrayCommands[1] == '7':
            strOut = wJSON.search_by_teacher(arrayCommands[0])
            strMore = 'всё расписание'
        else:
            try:
                arrayData = f.data_to_array(arrayCommands[1])
                date = datetime.datetime(int(arrayData[2]), int(arrayData[1]), int(arrayData[0]))
                strOut = wJSON.search_by_teacher_and_date(arrayCommands[0], wJSON.week_to_string(date.weekday()))
                strMore = 'расписание на: ' + arrayData[0] + '.' + arrayData[1] + '.' + arrayData[2]
            except:
                return 'ERROR'

        strDescipt = teacher.upper()
        return strOut
    else:
        return 'ERROR'
