

# Описание проекта:

Telegram-бот, о погоде и котиках. Позволяет просматривать фотографии случайных котиков, текущую погоду и прогноз на 5 дней для указанного города. 

## Используемый стек технологий:
- Python 3.9

## Порядок развертывания проекта:
1) Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:amartini1985/MyAlwaysGoodWeatherBot.git
```

```
cd MyAlwaysGoodWeatherBot

```

2) Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

3) Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

4) Инициировать базу данных запустив файл: initial_db.py.

5) Запустить файл: MyAlwaysGoodWeather.py 


## Автор проекта:
[Andrey Martyanov/amartini1985](https://github.com/amartini1985)
