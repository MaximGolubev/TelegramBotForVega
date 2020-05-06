import json


''' 
Это интерфейс для классов, которые будут получать данные 
Сейчас ваш провайдер - тестовый файл, но потом им может стать сервер,
поэтому выделяем этот кусок
'''


class AbstractProvider:
    def search_group(self, g):
        pass

    def search_subject(self, teacher):
        pass


class ServerProvider(AbstractProvider):
    pass


class FileProvider(AbstractProvider):

    def __init__(self, filename: str):
        with open(filename, 'r', encoding='utf-8') as file:
            self.data = json.load(file)

    def search_group(self, g):  # -Работает
        gr = text_to_group(g)
        if gr == 'ERROR':
            return 'ERROR'
        group = gr.upper()
        for gr in self.data['groups']:
            if gr['group'] == group:
                return json.dumps(gr['days'], indent=4, ensure_ascii=False)
        return 'ERROR'

    def search_subject(self, teacher):  # -Работает
        for pattern in self.data['patterns']:
            if 'pr' in pattern and not pattern['pr'] == '' and not pattern['pr'].upper().find(teacher.upper()) == -1:
                return pattern['search']
        return 'ERROR'


''' Этот класс будет преобразовывать куски JSON в текстовые данные '''


class JsonFormatter:
    def __init__(self, provider: FileProvider):
        self.provider = provider

    def search_group(self, group):
        return self.provider.search_group(group)

    def search_subject(self, teacher):
        return self.provider.search_subject(teacher)

    def search_by_group_and_date(self, group, dayWeek):  # -Работает
        groups = self.provider.search_group(group)
        jsonGroup = json.loads(groups)

        for day in jsonGroup:
            if day['day'] == dayWeek:
                return self.outputFormat(day)
        return 'Занятия отсутсвуют.'

    def search_by_group(self, group):  # -Работает
        arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        indexDay = 0
        timeTable = ''
        for day in arrayDays:
            text = self.search_by_group_and_date(group, day)
            if not text == 'Занятия отсутсвуют.':
                timeTable += text + '\n'
                indexDay += 1
            else:
                timeTable += arrayDays[indexDay] + ':\n'
                timeTable += text + '\n\n'
                indexDay += 1
        return timeTable

    def search_by_teacher_and_date(self, teacher, dayWeek):  # -Работает
        subject = self.provider.search_subject(teacher)
        if subject == 'ERROR':
            return 'Такого учителя нет.'
        arrayPars = [False, False, False, False, False, False, False]
        strTimeTable = ['', '', '', '', '', '', '']
        for gr in self.provider.data['groups']:
            for day in gr['days']:
                if day['day'] == dayWeek:
                    for lesson in day['pars']:
                        if lesson['name'] == subject:
                            numberLesson = int(lesson['number']) - 1
                            if arrayPars[numberLesson]:
                                strTimeTable[numberLesson] += ' | ' + gr['group']
                            else:
                                arrayPars[numberLesson] = True
                                strTimeTable[numberLesson] += f'{numberLesson + 1} - '
                                strTimeTable[numberLesson] += lesson['name'] + ' - '
                                strTimeTable[numberLesson] += lesson['place'] + ' - '
                                strTimeTable[numberLesson] += gr['group']

        timeTable = dayWeek + ':\n'
        for i in range(0, 7):
            if arrayPars[i]:
                timeTable += strTimeTable[i] + '\n'

        if timeTable == dayWeek + ':\n':
            return 'Занятия отсутствуют.'
        else:
            return timeTable

    def search_by_teacher(self, teacher):  # -Работает
        subject = self.provider.search_subject(teacher)
        if subject == 'ERROR':
            return 'Такого учителя нет.'

        arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        indexDay = 0
        timeTable = ''
        for day in arrayDays:
            s = self.search_by_teacher_and_date(teacher, day)
            if not s == 'Занятия отсутствуют.':
                timeTable += s + '\n'
                indexDay += 1
            else:
                timeTable += arrayDays[indexDay] + ':\n'
                timeTable += s + '\n\n'
                indexDay += 1
        return timeTable

    def print_all_time_table_with_course(self, strGroup, courseYear):
        timeTable = ''
        for group in self.provider.data['groups']:
            if not group['group'].find(courseYear) == -1 and not group['group'].find(strGroup) == -1:
                timeTable += group['group'] + '\n\n'
                timeTable += self.search_by_group(group['group']) + '\n\n'
        if timeTable == '':
            return 'ERROR'
        return timeTable

    def print_all_time_table(self):
        timeTable = ['', '', '', '', '', '']
        a = 0
        index = 0
        lastTwo = ''
        for group in self.provider.data['groups']:
            if lastTwo.find(str(group['group'])[8:]) == -1 and a != 0:
                index += 1
            timeTable[index] += group['group'] + '\n\n'
            timeTable[index] += self.search_by_group(group['group']) + '\n'
            lastTwo = str(group['group'])[8:]
            a += 1

        return timeTable

    def when_b209_is_free(self):
        countPars = [[0] * 7] * 7
        for i in range(0, 7):
            for j in range(0, 7):
                countPars[i][j] = 0
        arrayDays = ['ПН', 'ВТ', 'СР', 'ЧТ', 'ПТ', 'СБ', 'ВС']
        indexDay = 0

        for gr in self.provider.data['groups']:
            for day in gr['days']:
                for lesson in day['pars']:
                    indexPars = int(lesson['number']) - 1
                    if not lesson['place'].find('Б-209') == -1:
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
                    timeTable += f'{i + 1} - полностью свободна\n'
                elif count == 1:
                    timeTable += f'{i + 1} - свободна на половину\n'
                else:
                    timeTable += f'{i + 1} - занята\n'
            timeTable += '\n'
            indexDay += 1
        return timeTable

    # для query -----------------------------------------------------

    def search_teacher(self, teacher):  # -Работает
        teacher.upper()
        arrayTeachersOut = []
        for pattern in self.provider.data['patterns']:
            if 'pr' in pattern and not pattern['pr'] == '' and not pattern['pr'].upper().find(teacher) == -1:
                arrayTeachersOut.append(pattern['pr'])
        return arrayTeachersOut

    def search_group_by_one_part(self, strGr):
        group = strGr.upper()
        arrayGroupsOut = []
        for gr in self.provider.data['groups']:
            if gr['group'][0:4] == group:
                arrayGroupsOut.append(gr['group'])
        return arrayGroupsOut

    def search_group_by_two_parts(self, strGr, strOne):
        arrayGroupsIn = self.search_group_by_one_part(strGr)
        l = len(arrayGroupsIn)
        arrayGroupsOut = []
        for i in range(0, l):
            if not arrayGroupsIn[i][5:7].find(strOne) == -1:
                arrayGroupsOut.append(arrayGroupsIn[i])
        return arrayGroupsOut

    def search_group_by_three_parts(self, strGr, strOne, strTwo):
        arrayGroupsIn = self.search_group_by_two_parts(strGr, strOne)
        l = len(arrayGroupsIn)
        arrayGroupsOut = []
        for i in range(0, l):
            if not arrayGroupsIn[i][8:].find(strTwo) == -1:
                arrayGroupsOut.append(arrayGroupsIn[i])
        return arrayGroupsOut

    def outputFormat(self, jsonDay):
        strTimeTable = ['', '', '', '', '', '', '']
        for lesson in jsonDay['pars']:
            numberLesson = lesson['number'] - 1
            strTimeTable[numberLesson] += str(lesson["number"]) + ' - '
            strTimeTable[numberLesson] += lesson['name'] + ' - '
            strTimeTable[numberLesson] += lesson['place'] + '\n'

        dayTimeTable = jsonDay['day'] + ':\n'
        for i in range(0, 7):
            dayTimeTable += strTimeTable[i]
            if strTimeTable[i] == '':
                dayTimeTable += f'{i + 1} - '
                dayTimeTable += 'пусто\n'
        return dayTimeTable

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


def text_to_group(text):
    if len(text) == 10:
        gr = text[:4] + "-" + text[5:7] + "-" + text[8:]
    elif len(text) == 8:
        gr = text[:4] + "-" + text[4:6] + "-" + text[6:]
    else:
        return 'ERROR'
    return gr

