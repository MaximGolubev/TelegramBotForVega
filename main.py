import config
import functions as fnc
import strings
import keyboard as kb
import inlineRealization as iRz
import workWithDataBase as wDB

import telebot
from telebot.types import Message
import logging


# TOKEN = os.environ.get('TELEGRAM_BOT_FOR_VEGA_TOKEN')
TOKEN = config.token
LOG_FORMAT = '%(funcName)s :: %(message)s'
# API_URL = f'https://api.telegram.org/bot{TOKEN}'

# apihelper.proxy = {'https': 'https://96.96.33.133:1080'}

bot = telebot.TeleBot(TOKEN)
loggerDEBUG = logging.getLogger('logger_debug')
loggerDEBUG.setLevel('DEBUG')

logging.getLogger('urllib3').setLevel('ERROR')
logging.getLogger('TeleBot').setLevel('ERROR')
logging.getLogger('socks').setLevel('ERROR')
logging.getLogger('requests').setLevel('ERROR')
# loggerDEBUG.addHandler()

# wDB.init_data_base()
dataBase = wDB.FileDBWork("USERS_DATA_BASE.db", "ADMINS_DATA_BASE.db")
logging.basicConfig(level='DEBUG', filename='log.txt', format=LOG_FORMAT)


@bot.message_handler(commands=['start'])
def process_start_command(message: Message):
    # loggerDEBUG.debug(f'/start {message.from_user.username}')
    bot.send_message(message.from_user.id,
                     '\n'.join([f'Привет, {message.from_user.username}!',
                                'Выберите:']),
                     reply_markup=kb.choiceMarkup)
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    loggerDEBUG.debug(f'/start {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(commands=['setnew'])
def time_table_changed(message: Message):
    # loggerDEBUG.debug(f'/setnew {message.from_user.username}')
    if fnc.isAdmin(message.from_user.id):
        s = message.text.split(' ')
        option = ''
        if len(s) > 1:
            for i in range(1, len(s)):
                option += s[i] + ' '
        fnc.sendNotif(option)
        loggerDEBUG.debug(f'/setnew {message.from_user.username} - {message.from_user.id} - {option}')
    else:
        loggerDEBUG.warning('\n'.join([f'/setnew ----- ВНИМАНИЕ!!! ',
                                       f'пользователь, НЕ ЯВЛЯЮЩИЙСЯ АДМИНОМ использовал /setnew',
                                       f'chat_id: {message.from_user.id}',
                                       f'username: {message.from_user.username}']))


@bot.message_handler(commands=['help'])
def send_list_of_commands(message: Message):
    # loggerDEBUG.debug(f'/help {message.from_user.username}')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    bot.send_message(message.chat.id, strings.INSTROUCTIONS_HELP)
    loggerDEBUG.debug(f'/help {message.from_user.username} - {message.from_user.id}')


@bot.message_handler(content_types=['text'])
def repeat_message(message: Message):
    loggerDEBUG.debug(f'/text {message.from_user.username}')
    dataBase.add_user(user_id=message.from_user.id, chat_id=message.chat.id)
    fnc.general_func(message)
    loggerDEBUG.debug(f'/help {message.from_user.username} - {message.from_user.id} - "{message.text}"')


@bot.inline_handler(func=lambda query: len(query.query) > 0)
def query_text(query):
    loggerDEBUG.debug(f'QUERY: {query.query}')
    strOut = iRz.general_func(query)
    bot.answer_inline_query(query.id, strOut)


if __name__ == '__main__':
    bot.polling(none_stop=True)
