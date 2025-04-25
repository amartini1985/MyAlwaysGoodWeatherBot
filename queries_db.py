import sqlite3


def add_cities(name, lat, lot):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''INSERT INTO cities(name, lat, lon) VALUES (?, ?, ?);'''
    cur.execute(query, (name, lat, lot))
    con.commit()
    con.close()


def get_city_from_db(city):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''SELECT lat, lon FROM cities WHERE name=?;'''
    result = cur.execute(query, (city,)).fetchone()
    con.close()
    return result


def get_url_weather(city='Москва'):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''SELECT lat, lon FROM cities WHERE name=?;'''
    result = cur.execute(query, (city,))
    lat, lot = result.fetchone()
    con.close()
    return f'https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lot}&appid=b7350d7f981ddf7daeffedb79e4d71d8&lang=ru'


def get_url_forecast(city='Москва'):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''SELECT lat, lon FROM cities WHERE name=?;'''
    result = cur.execute(query, (city,))
    lat, lot = result.fetchone()
    con.close()
    return f'https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lot}&appid=b7350d7f981ddf7daeffedb79e4d71d8&lang=ru'


def insert_data(user, chat, date_query):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''INSERT INTO statistic(user, chat, date_query) VALUES (?, ?, ?);'''
    cur.execute(query, (user, chat, date_query))
    con.commit()
    con.close()


def set_chat_city(city, chat_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''INSERT INTO current_city(city, chat) VALUES (?, ?);'''
    cur.execute(query, (city, chat_id))
    con.commit()
    con.close()


def get_chat_city(chat_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''SELECT city FROM current_city WHERE chat=?;'''
    result = cur.execute(query, (chat_id,)).fetchone()
    if not result:
        query = '''INSERT INTO current_city(city, chat) VALUES (?, ?);'''
        cur.execute(query, ('Moscow', chat_id))
        con.commit()
        result = ('Moscow',)
    con.close()
    return result


def del_chat_city(chat_id):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''DELETE FROM current_city WHERE chat=?;'''
    cur.execute(query, (chat_id,))
    con.commit()
    con.close()


def get_statistics():
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''SELECT user, COUNT(*) FROM statistic GROUP BY user;'''
    result = cur.execute(query).fetchall()
    con.close()
    return result
