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
choiceMarkup.row(strings.SEARCH_BY_TEACHER)
choiceMarkup.row(strings.SEARCH_ALL_TIME_TABLE)
choiceMarkup.row(strings.SEARCH_BY_B209)

choiceCourse = telebot.types.ReplyKeyboardMarkup(1)
number = determine_the_year()
STRBUTTONSTHIRD_1 = "20" + str(number) + " (бакалавриат)"
STRBUTTONSTHIRD_2 = "20" + str(number - 1) + " (бакалавриат)"
STRBUTTONSTHIRD_3 = "20" + str(number - 2) + " (бакалавриат)"
STRBUTTONSTHIRD_4 = "20" + str(number - 3) + " (бакалавриат)"
STRBUTTONSTHIRD_5 = "20" + str(number) + " (магистратура)"
STRBUTTONSTHIRD_6 = "20" + str(number - 1) + " (магистратура)"
STRBUTTONSTHIRD_7 = "все"
STRBUTTONSTHIRD_8 = "выйти"

choiceCourse.row(STRBUTTONSTHIRD_1, STRBUTTONSTHIRD_2)
choiceCourse.row(STRBUTTONSTHIRD_3, STRBUTTONSTHIRD_4)
choiceCourse.row(STRBUTTONSTHIRD_5, STRBUTTONSTHIRD_6)
choiceCourse.row(STRBUTTONSTHIRD_7)
choiceCourse.row(STRBUTTONSTHIRD_8)
