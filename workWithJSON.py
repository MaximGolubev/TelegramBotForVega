import json


with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


def search_group(group): #-Работает
    group = group.upper()
    for gr in data['groups']:
        if gr['group'] == group:
            return json.dumps(gr['days'], indent=4, ensure_ascii=False)
    return 'ERROR'


def search_by_group_and_date(group, dayWeek): #-Работает
    groups = search_group(group)
    jsonGroup = json.loads(groups)

    for day in jsonGroup:
        if day['day'] == dayWeek:
            return outputFormat(day)
    return 'Занятия отсутсвуют.'


def search_by_group(group): #-Работает
    arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    indexDay = 0
    timeTable = ''
    for day in arrayDays:
        text = search_by_group_and_date(group, day)
        if not text == 'Занятия отсутсвуют.':
            #timeTable += arrayDays[indexDay] + '\n'
            timeTable += text + '\n'
            indexDay +=1
        else:
            timeTable += arrayDays[indexDay] + ':\n'
            timeTable += text + '\n\n'
            indexDay += 1
    return timeTable


def search_subject(teacher): #-Работает
    for pattern in data['patterns']:
        if not pattern['pr'] == '' and not pattern['pr'].upper().find(teacher.upper()) == -1:
            print("Учитель существует")
            print(pattern['search'])
            return pattern['search']
    return 'ERROR'


def search_by_teacher_and_date(teacher, dayWeek): #-Работает
    subject = search_subject(teacher)
    if subject == 'ERROR':
        return 'Такого учителя нет.'
    arrayPars = [False, False, False, False, False, False, False]
    strTimeTable = ['', '', '', '', '', '', '']
    for gr in data['groups']:
        #print(gr['group'])
        for day in gr['days']:
            if day['day'] == dayWeek:
                #print('\t' + day['day'])
                for lesson in day['pars']:
                    #print('\t' + '\t' + lesson['name'])
                    if lesson['name'] == subject:
                        numberLesson = int(lesson['number']) - 1
                        if arrayPars[numberLesson]:
                            strTimeTable[numberLesson] += ' | ' + gr['group']
                        else:
                            arrayPars[numberLesson] = True
                            strTimeTable[numberLesson] += str(numberLesson + 1) + ' - '
                            strTimeTable[numberLesson] += lesson['name'] + ' - '
                            strTimeTable[numberLesson] += lesson['place'] + ' - '
                            strTimeTable[numberLesson] += gr['group']
                            #print('\t' + '\t' + '\t' + strTimeTable[numberLesson])

    timeTable = dayWeek + ':\n'
    for i in range(0, 7):
        if arrayPars[i]:
            timeTable += strTimeTable[i] + '\n'


    if timeTable == dayWeek + ':\n':
        return 'Занятия отсутствуют.'
    else:
        #print(timeTable)
        return timeTable


def search_by_teacher(teacher): #-Работает
    subject = search_subject(teacher)
    if subject == 'ERROR':
        return 'Такого учителя нет.'

    arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    indexDay = 0
    timeTable = ''
    for day in arrayDays:
        str = search_by_teacher_and_date(teacher, day)
        if not str == 'Занятия отсутствуют.':
            timeTable += str + '\n'
            indexDay += 1
        else:
            timeTable += arrayDays[indexDay] + ':\n'
            timeTable += str + '\n\n'
            indexDay += 1
    return timeTable


def print_all_time_table_with_course(courseYear):
    timeTable = ''
    for group in data['groups']:
        if not group['group'].find(courseYear) == -1:
            timeTable += group['group'] + '\n\n'
            timeTable += search_by_group(group['group']) + '\n\n'
    if timeTable == '':
        return 'ERROR'
    return timeTable


def print_all_time_table():
    timeTable = ''
    for group in data['groups']:
        timeTable += group['group'] + '\n\n'
        timeTable += search_by_group(group['group']) + '\n'
        #print(timeTable)
    return timeTable


#------------------ВТОРОСТЕПЕННЫЕ ФУНКЦИИ------------------


def week_to_string(codeDayWeek):
        if codeDayWeek == 0:
            return 'ПН'
        elif codeDayWeek == 1:
            return 'ВТ'
        elif codeDayWeek == 2:
            return 'СР'
        elif codeDayWeek == 3:
            return 'ЧТ'
        elif codeDayWeek == 4:
            return 'ПТ'
        elif codeDayWeek == 5:
            return 'СБ'
        else:
            return 'ВС'


def outputFormat(jsonDay):
    strTimeTable = ['', '', '', '', '', '', '']
    for lesson in jsonDay['pars']:
        numberLesson = lesson['number']-1
        strTimeTable[numberLesson] += str(lesson['number']) + ' - '
        strTimeTable[numberLesson] += lesson['name'] + ' - '
        strTimeTable[numberLesson] += lesson['place'] + '\n'

    dayTimeTable = jsonDay['day'] + ':\n'
    for i in range(0, 7):
        dayTimeTable += strTimeTable[i]
        if strTimeTable[i] == '':
            dayTimeTable += str(i+1) + ' - '
            dayTimeTable += 'пусто\n'
    #print(dayTimeTable)
    return dayTimeTable