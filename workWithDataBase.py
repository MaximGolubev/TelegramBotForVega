import sqlite3


CONNECTION = None


def get_connection():
    global CONNECTION
    if CONNECTION is None:
        CONNECTION = sqlite3.connect('USERS_DATA_BASE.db', check_same_thread=False)
    return CONNECTION


def init_data_base(force: bool = False):
    connection = get_connection()
    c = connection.cursor()

    if force:
        c.execute('DROP TABLE IF EXISTS all_users_chat_id')

    c.execute("""CREATE TABLE IF NOT EXISTS all_users_chat_id
            (id         INTEGER PRIMARY KEY, 
            chat_id     INTEGER NOT NULL)
            """)

    connection.commit()


def add_user(chat_id: int):
    connection = get_connection()
    c = connection.cursor()
    c.execute('INSERT INTO all_users_chat_id (chat_id) VALUES (?)', (chat_id,))
    connection.commit()

