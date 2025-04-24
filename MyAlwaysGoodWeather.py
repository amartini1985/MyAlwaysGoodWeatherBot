import os
import requests
from telebot import TeleBot, types
from dotenv import load_dotenv
from pprint import pprint
from datetime import date, datetime
import locale
from utils_functions import kelvin_to_celsius, pascal_to_mmrs
import sqlite3

load_dotenv()

secret_code = os.getenv('TOKEN')
bot = TeleBot(token=secret_code)

URL_CAT = 'https://api.thecatapi.com/v1/images/search'

URL_WEATHER = 'https://api.openweathermap.org/data/2.5/weather?lat=55.7522&lon=37.6156&appid=b7350d7f981ddf7daeffedb79e4d71d8&lang=ru'

URL_FORECAST = 'https://api.openweathermap.org/data/2.5/forecast?lat=55.7522&lon=37.6156&appid=b7350d7f981ddf7daeffedb79e4d71d8&lang=ru'

#URL_FORECAST = 'https://api.openweathermap.org/data/2.5/forecast/daily?lat=44.34&lon=10.99&cnt=7&appid=b7350d7f981ddf7daeffedb79e4d71d8'

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8') # вывод даты в формате RU


con = sqlite3.connect('db.sqlite')

cur = con.cursor()

query_1 = '''
CREATE TABLE IF NOT EXISTS statistic(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    chat INTEGER,
    date_query TEXT
);
'''
cur.execute(query_1)


con.close() 


def insert_data(user, chat, date_query):
    con = sqlite3.connect('db.sqlite')
    cur = con.cursor()
    query = '''
    INSERT INTO statistic(user, chat, date_query) VALUES (?, ?, ?);
    '''
    cur.execute(query, (user, chat, date_query))
    con.commit()
    con.close()



def get_new_image():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        print(error)
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_current_weather():
    response = requests.get(URL_WEATHER).json()
    return response

def get_forcast_weather():
    response = requests.get(URL_FORECAST).json()
    return response


def message_weather(weather):
    weather = weather()
    pprint(weather)
    city = weather['name'].capitalize()
    description = weather["weather"][0]["description"].capitalize()
    temp_min = kelvin_to_celsius(weather["main"]["temp_min"])
    temp_max = kelvin_to_celsius(weather["main"]["temp_max"])
    speed_wind = weather['wind']['speed']
    pressure = pascal_to_mmrs(weather["main"]["pressure"])
    message = (f'<b>{date.today().strftime("%d %B %Y (%A)")}</b>\n'
               f'<b>{city}</b>\n'
               f'{description}\n'
               f'Температура: {temp_min} - {temp_max}°C\n'
               f'Давление: {pressure} мм.рт.ст\n'
               f'Ветер: {speed_wind} м/c'
               )
    return message


def message_forecast(weather):
    weather = weather()
    city = weather['city']['name']
    weather_list = filter(lambda x: datetime.fromtimestamp(x['dt']).hour == 15, weather['list'])
    message = f'<b>{city}</b>\n\n'
    for weather in weather_list:
        description = weather["weather"][0]["description"].capitalize()
        temp_min = kelvin_to_celsius(weather["main"]["temp_min"])
        temp_max = kelvin_to_celsius(weather["main"]["temp_max"])
        speed_wind = weather['wind']['speed']
        message += (f'<b>{datetime.fromtimestamp(weather["dt"]).strftime("%d %B %Y (%A)")}</b>\n'
                f'{description}\n'
                f'Температура: {temp_min} - {temp_max}°C\n'
                f'Ветер: {speed_wind} м/c\n\n'
                )
    return message

@bot.message_handler(commands=['\U0001F63A'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())


@bot.message_handler(commands=['\U00002600'])
def current_weather(message):
    chat = message.chat
    bot.send_message(chat.id, text=message_weather(get_current_weather), parse_mode="html")
    insert_data(chat.first_name, chat.id, date.today().strftime('%d-%m-%Y'))


@bot.message_handler(commands=['forecast'])
def forecast(message):
    chat = message.chat
    bot.send_message(chat.id, text=message_forecast(get_forcast_weather), parse_mode="html")


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton('/\U0001F63A'), types.KeyboardButton('/\U00002600'))
    keyboard.row(types.KeyboardButton('/forecast'))
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text=f'Спасибо, что вы включили меня, {name}!', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(chat_id=chat_id, text='Привет, я чат с котиками и погодой!')


def main():
    bot.polling()


if __name__ == '__main__':
    main()
