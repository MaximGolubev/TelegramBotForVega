import telebot



choiceMarkup = telebot.types.ReplyKeyboardMarkup(1)
choiceMarkup.row("Поиск по группе")
choiceMarkup.row("Поиск по подгруппе")
choiceMarkup.row("Поиск по преподавателю")
choiceMarkup.row("Вывод полного расписания")

