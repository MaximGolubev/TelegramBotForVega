import sqlite3

CONNECTION_USERS_DB = None
CONNECTION_ADMINS_DB = None


def get_connection_to_users_data_base():
    global CONNECTION_USERS_DB
    if CONNECTION_USERS_DB is None:
        CONNECTION_USERS_DB = sqlite3.connect('USERS_DATA_BASE.db', check_same_thread=False)
    return CONNECTION_USERS_DB


def get_connection_to_admin_data_base():
    global CONNECTION_ADMINS_DB
    if CONNECTION_ADMINS_DB is None:
        CONNECTION_ADMINS_DB = sqlite3.connect('ADMINS_DATA_BASE.db', check_same_thread=False)
    return CONNECTION_ADMINS_DB


def init_data_base(force: bool = False):
    users_connection = get_connection_to_users_data_base()
    c = users_connection.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS all_users_chat_id')
    c.execute("""CREATE TABLE IF NOT EXISTS all_users_chat_id
            (id         INTEGER PRIMARY KEY, 
            chat_id     INTEGER NOT NULL UNIQUE)
            """)
    users_connection.commit()

    admins_connection = get_connection_to_admin_data_base()
    c = admins_connection.cursor()
    if force:
        c.execute('DROP TABLE IF EXISTS admins_chat_id')
    c.execute("""CREATE TABLE IF NOT EXISTS admins_chat_id
                (id         INTEGER PRIMARY KEY, 
                chat_id     INTEGER NOT NULL UNIQUE)
                """)
    admins_connection.commit()


def add_user(chat_id: int):
    connection = get_connection_to_users_data_base()
    c = connection.cursor()
    try:
        c.execute('INSERT INTO all_users_chat_id (chat_id) VALUES (?)', (chat_id,))
        connection.commit()
        print("----- DATA-BASE новый chat_id: '" + str(chat_id) + "'")
    except:
        print("----- DATA-BASE chat_id: '" + str(chat_id) + "' уже сущетсвует")


def user_from_data_base(dataBase, index):
    user = -1
    [user], = dataBase.execute('select name from all_users_chat_id where id=?', (index,))
    return user
