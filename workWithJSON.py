import json

# тут все оборачиваем в классы
# примерно так, но надо будет шлифовать


''' 
Это интерфейс для классов, которые будут получать данные 
Сейчас ваш провайдер - тестовый файл, но потом им может стать сервер,
поэтому выделяем этот кусок
'''


class AbstractProvider:
    # тут опишите методы, которые вам нужны: search_group и т.д.
    def search_group(self, group):
        pass


class FileProvider(AbstractProvider):
    # тут реализация методов интерфейса
    def __init__(self):
        with open('dataTest.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

    def search_group(self, group):
        pass


''' Этот класс будет преобразовывать куски JSON в текстовые данные '''


class JsonFormatter:
    # используем иньекцию зависимостей (Dependency Injection):
    # за поставку данных отвечает другой объект, когда появится API - воткнем сервак
    def __init__(self, provider: AbstractProvider):
        self.provider = provider
        # ...






def search_group(g):  # -Работает
    gr = text_to_group(g)
    if gr == 'ERROR':
        return 'ERROR'
    group = gr.upper()
    for gr in data['groups']:
        if gr['group'] == group:
            return json.dumps(gr['days'], indent=4, ensure_ascii=False)
    return 'ERROR'


def search_by_group_and_date(group, dayWeek):  # -Работает
    groups = search_group(group)
    jsonGroup = json.loads(groups)

    for day in jsonGroup:
        if day['day'] == dayWeek:
            return outputFormat(day)
    return 'Занятия отсутсвуют.'


def search_by_group(group):  # -Работает
    arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    indexDay = 0
    timeTable = ''
    for day in arrayDays:
        text = search_by_group_and_date(group, day)
        if not text == 'Занятия отсутсвуют.':
            # timeTable += arrayDays[indexDay] + '\n'
            timeTable += text + '\n'
            indexDay += 1
        else:
            timeTable += arrayDays[indexDay] + ':\n'
            timeTable += text + '\n\n'
            indexDay += 1
    return timeTable


def search_subject(teacher):  # -Работает
    for pattern in data['patterns']:
        if 'pr' in pattern and not pattern['pr'] == '' and not pattern['pr'].upper().find(teacher.upper()) == -1:
            #print("Учитель существует")
            #print(pattern['search'])
            return pattern['search']
    return 'ERROR'


def search_by_teacher_and_date(teacher, dayWeek):  # -Работает
    subject = search_subject(teacher)
    if subject == 'ERROR':
        return 'Такого учителя нет.'
    arrayPars = [False, False, False, False, False, False, False]
    strTimeTable = ['', '', '', '', '', '', '']
    for gr in data['groups']:
        # print(gr['group'])
        for day in gr['days']:
            if day['day'] == dayWeek:
                # print('\t' + day['day'])
                for lesson in day['pars']:
                    # print('\t' + '\t' + lesson['name'])
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
                            # print('\t' + '\t' + '\t' + strTimeTable[numberLesson])

    timeTable = dayWeek + ':\n'
    for i in range(0, 7):
        if arrayPars[i]:
            timeTable += strTimeTable[i] + '\n'

    if timeTable == dayWeek + ':\n':
        return 'Занятия отсутствуют.'
    else:
        # print(timeTable)
        return timeTable


def search_by_teacher(teacher):  # -Работает
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


def print_all_time_table_with_course(strGroup, courseYear):
    timeTable = ''
    for group in data['groups']:
        if not group['group'].find(courseYear) == -1 and not group['group'].find(strGroup) == -1:
            timeTable += group['group'] + '\n\n'
            timeTable += search_by_group(group['group']) + '\n\n'
    if timeTable == '':
        return 'ERROR'
    return timeTable


def print_all_time_table():
    timeTable = ['', '', '', '', '', '']
    a = 0
    index = 0
    lastTwo = ''
    for group in data['groups']:
        if lastTwo.find(str(group['group'])[8:]) == -1 and a != 0:
            # print("zashel = " + str(index) + " - " + str(group['group']))
            index += 1
        timeTable[index] += group['group'] + '\n\n'
        timeTable[index] += search_by_group(group['group']) + '\n'
        lastTwo = str(group['group'])[8:]
        a += 1

    return timeTable


def when_b209_is_free():
    countPars = [[0] * 7] * 7
    for i in range(0, 7):
        for j in range(0, 7):
            countPars[i][j] = 0
    arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
    indexDay = 0

    for gr in data['groups']:
        # print(gr['group'])
        for day in gr['days']:
            for lesson in day['pars']:
                indexPars = int(lesson['number']) - 1
                if not lesson['place'].find('Б-209') == -1:
                    print(arrayDays[indexDay] + " " + str(indexPars + 1))
                    countPars[indexDay][indexPars] += 1
            indexDay += 1
        indexDay = 0

    timeTable = ''
    indexDay = 0
    for dayWeek in arrayDays:
        timeTable += dayWeek + ':\n'
        for i in range(0, 7):
            count = countPars[indexDay][i]
            if count == 0:
                timeTable += str(i + 1) + " - полностью свободна" + '\n'
            elif count == 1:
                timeTable += str(i + 1) + " - свободна на половину" + '\n'
            else:
                timeTable += str(i + 1) + " - занята" + '\n'
        timeTable += '\n'
        indexDay += 1
    return timeTable


# ------------------ВТОРОСТЕПЕННЫЕ ФУНКЦИИ------------------


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
        numberLesson = lesson['number'] - 1
        strTimeTable[numberLesson] += str(lesson['number']) + ' - '
        strTimeTable[numberLesson] += lesson['name'] + ' - '
        strTimeTable[numberLesson] += lesson['place'] + '\n'

    dayTimeTable = jsonDay['day'] + ':\n'
    for i in range(0, 7):
        dayTimeTable += strTimeTable[i]
        if strTimeTable[i] == '':
            dayTimeTable += str(i + 1) + ' - '
            dayTimeTable += 'пусто\n'
    # print(dayTimeTable)
    return dayTimeTable


def text_to_group(text):
    if len(text) == 10:
        gr = text[:4] + "-" + text[5:7] + "-" + text[8:]
    elif len(text) == 8:
        gr = text[:4] + "-" + text[4:6] + "-" + text[6:]
    else:
        return 'ERROR'
    return gr


def search_teacher(teacher):  # -Работает
    teacher.upper()
    arrayTeachersOut = []
    #print('\t' + teacher + ': ')
    for pattern in data['patterns']:
        if 'pr' in pattern and not pattern['pr'] == '' and not pattern['pr'].upper().find(teacher) == -1:
            arrayTeachersOut.append(pattern['pr'])
            #print('\t\t' + pattern['pr'])
    return arrayTeachersOut


def search_group_by_one_part(strGr):
    group = strGr.upper()
    arrayGroupsOut = []
    #print('\t' + strGr + ': ')
    for gr in data['groups']:
        if gr['group'][0:4] == group:
            arrayGroupsOut.append(gr['group'])
            #print('\t\t' + gr['group'])
    return arrayGroupsOut


def search_group_by_two_parts(strGr, strOne):
    arrayGroupsIn = search_group_by_one_part(strGr)
    l = len(arrayGroupsIn)
    arrayGroupsOut = []
    #print('\t' + strGr + '-' + strOne + ': ')
    for i in range(0, l):
        if not arrayGroupsIn[i][5:7].find(strOne) == -1:
            arrayGroupsOut.append(arrayGroupsIn[i])
            #print('\t\t' + arrayGroupsIn[i])
    return arrayGroupsOut


def search_group_by_three_parts(strGr, strOne, strTwo):
    arrayGroupsIn = search_group_by_two_parts(strGr, strOne)
    l = len(arrayGroupsIn)
    arrayGroupsOut = []
    #print('\t' + strGr + '-' + strOne + '-' + strTwo + ': ')
    for i in range(0, l):
        if not arrayGroupsIn[i][8:].find(strTwo) == -1:
            arrayGroupsOut.append(arrayGroupsIn[i])
            #print('\t\t' + arrayGroupsIn[i])
    return arrayGroupsOut
