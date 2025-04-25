import locale
import os
import requests

from datetime import date, datetime
from dotenv import load_dotenv
from googletrans import Translator
from telebot import TeleBot, types

from queries_db import (
    add_cities, del_chat_city, insert_data,
    get_city_from_db, get_chat_city, get_statistics,
    get_url_forecast, get_url_weather, set_chat_city
)
from utils_functions import kelvin_to_celsius, pascal_to_mmrs

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

load_dotenv()

translator = Translator()

URL_CAT = 'https://api.thecatapi.com/v1/images/search'

bot = TeleBot(token=os.getenv('TOKEN'))


def translate_city(city_name):
    translation = translator.translate(city_name, dest='en').text
    return translation


def set_city(city, chat_id):
    name, lat, lon = city[0]['name'], city[0]['lat'], city[0]['lon']
    if not get_city_from_db(name):
        add_cities(name, lat, lon)
    current_city = get_chat_city(chat_id)
    if current_city is None:
        set_chat_city(name, chat_id)
    else:
        if current_city[0] != name:
            del_chat_city(chat_id)
            set_chat_city(name, chat_id)


def get_new_image():
    try:
        response = requests.get(URL_CAT)
    except Exception:
        new_url = 'https://api.thedogapi.com/v1/images/search'
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat


def get_current_weather(chat_id):
    city = get_chat_city(chat_id)[0]
    response = requests.get(get_url_weather(city)).json()
    return response


def get_forcast_weather(chat_id):
    city = get_chat_city(chat_id)[0]
    response = requests.get(get_url_forecast(city)).json()
    return response


def get_city(city):
    response = requests.get(f'http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=5&appid=b7350d7f981ddf7daeffedb79e4d71d8&lang=ru').json()
    return response


def message_weather(weather):
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
    city = weather['city']['name']
    weather_list = filter(
        lambda x: datetime.fromtimestamp(x['dt']).hour == 15, weather['list'])
    message = f'<b>{city}</b>\n\n'
    for weather in weather_list:
        description = weather["weather"][0]["description"].capitalize()
        temp_max = kelvin_to_celsius(weather["main"]["temp_max"])
        speed_wind = weather['wind']['speed']
        message += (
            f'<b>{datetime.fromtimestamp(weather["dt"]).strftime("%d %B %Y (%A)")}</b>\n'
            f'{description}\n'
            f'Температура: {temp_max}°C\n'
            f'Ветер: {speed_wind} м/c\n\n'
        )
    return message


def message_help():
    return (
        '<b>Это бот о погоде и котиках \U0001F63A \U00002600\n</b>'
        ' Для показа котиков нажмите "\U0001F63A"\n'
        ' Для просмотра текущей погоды нажмите "\U00002600"\n'
        ' Для просмотра прогноза нажмите \\forecast\n'
        ' Для смены города введите название города на русском\n'
        ' Автор: https://t.me/amartini1985'
        )


def message_statistics(messages):
    message = ''
    for mes in messages:
        message += f'{mes[0]} - {mes[1]}\n'
    return message


@bot.message_handler(commands=['\U0001F63A'])
def new_cat(message):
    chat = message.chat
    bot.send_photo(chat.id, get_new_image())
    insert_data(chat.first_name, chat.id, date.today().strftime('%d-%m-%Y'))


@bot.message_handler(commands=['\U00002600'])
def current_weather(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(
        chat_id, text=message_weather(get_current_weather(chat_id)),
        parse_mode="html")
    insert_data(chat.first_name, chat.id, date.today().strftime('%d-%m-%Y'))


@bot.message_handler(commands=['forecast'])
def forecast(message):
    chat = message.chat
    chat_id = chat.id
    bot.send_message(
        chat.id, text=message_forecast(get_forcast_weather(chat_id)),
        parse_mode="html")
    insert_data(chat.first_name, chat.id, date.today().strftime('%d-%m-%Y'))


@bot.message_handler(commands=['help'])
def help(message):
    chat = message.chat
    bot.send_message(chat.id, text=message_help(), parse_mode="html")


@bot.message_handler(commands=['statistics'])
def statistic(message):
    chat = message.chat
    bot.send_message(
        chat.id, text=message_statistics(get_statistics()),
        parse_mode="html")


@bot.message_handler(commands=['start'])
def wake_up(message):
    chat = message.chat
    name = chat.first_name
    chat_id = chat.id
    set_city(get_city('Moscow'), chat_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton('/\U0001F63A'),
        types.KeyboardButton('/\U00002600'))
    keyboard.row(
        types.KeyboardButton('/forecast'),
        types.KeyboardButton('/help'))
    bot.send_message(
        chat_id=chat_id,
        text=f'Спасибо, что вы включили меня, {name}!',
        reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def say_hi(message):
    chat = message.chat
    chat_id = chat.id
    text = message.text
    city = get_city(translate_city(text))
    if city:
        bot.send_message(
            chat_id=chat_id,
            text=f'Вы выбрали город {text}')
        set_city(city, chat_id)
    else:
        bot.send_message(
            chat_id=chat_id,
            text='Вы указали несуществующий город')


def main():
    bot.polling(5)


if __name__ == '__main__':
    main()
