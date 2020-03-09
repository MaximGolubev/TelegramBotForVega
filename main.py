from telebot.types import Message
#from telebot import apihelper
import config
import telebot

BOT = telebot.TeleBot(config.token)
TOKEN = config.token
#PROXY =

#apihelper.proxy = {'https': PROXY}


@BOT.message_handler(commands=['start'])
def send_welcome(message):
    BOT.send_message(message.chat.id,
                     "Hello, " + message.from_user.first_name + " " + message.from_user.last_name + "!")


@BOT.message_handler(commands=['help'])
def send_welcome(message: Message):
    BOT.send_message(message.chat.id, "start - начало беседы с ботом\nhelp - полный список команд\nspecialInformation "
                                      "- дополнительная информация")


@BOT.message_handler(commands=['specialInformation'])
def send_special_inf(message):
    BOT.send_message(message.chat.id, "Ваш логин: " + str(message.from_user.username) + "\nВаш Id: " + str(
        message.from_user.id) + "\nId чата: " + str(message.chat.id))


@BOT.message_handler(func=lambda message: True)
def repeat_all_messages(message: Message):
    BOT.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    BOT.polling(none_stop=True)
