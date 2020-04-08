import strings
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
choiceMarkup.row(strings.SEARCH_BY_GROUP)
choiceMarkup.row(strings.SEARCH_BY_SUBGROUP)
choiceMarkup.row(strings.SEARCH_BY_TEACHER)
choiceMarkup.row(strings.SEARCH_ALL_TIME_TABLE)

choiceCourse = telebot.types.ReplyKeyboardMarkup(1)
number = determine_the_year()
choiceCourse.row("20" + str(number), "20" + str(number - 1))
choiceCourse.row("20" + str(number - 2), "20" + str(number - 3))
choiceCourse.row("все")
choiceCourse.row("выйти")
