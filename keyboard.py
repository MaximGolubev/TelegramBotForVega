import telebot
import datetime


def determine_the_year():
    month = datetime.datetime.today().month
    if month == 9 or month == 10 or month == 11 or month == 12:
        number = datetime.datetime.today().year % 100
    else:
        number = datetime.datetime.today().year % 100 - 1
    return number


choiceMarkup = telebot.types.ReplyKeyboardMarkup(1)
choiceMarkup.row("Поиск по группе")
choiceMarkup.row("Поиск по подгруппе")
choiceMarkup.row("Поиск по преподавателю")
choiceMarkup.row("Вывод полного расписания")

choiceCourse = telebot.types.ReplyKeyboardMarkup(1)
number = determine_the_year()
choiceCourse.row("20" + str(number), "20" + str(number + 1))
choiceCourse.row("20" + str(number + 2), "20" + str(number + 3))
choiceCourse.row("20" + str(number + 4), "20" + str(number + 5))
choiceCourse.row("все")
choiceCourse.row("выйти")
