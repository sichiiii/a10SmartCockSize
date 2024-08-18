import time
import random
import telebot
import sqlite3
import threading

from telebot import types
from app_logger import get_logger
from create_dicpic import generate_pillar_image

logger = get_logger(__name__)
db_connections = threading.local()

percentages = [3.3, 1.3, 7.4, 23.4, 35.8, 21.4, 6.9, 0.5]
length_ranges = [(7, 11), (11, 12), (12, 14), (14, 16.5), (16.5, 17.5), (17.5, 20), (20, 23), (23, 27)]
width_ranges = [(2.22, 2.41), (2.41, 2.8), (2.8, 3.18), (3.18, 3.58), (3.58, 3.97), (3.97, 4.39), (4.39, 4.77), (4.77, 6.33)]

roles = ["гейский", "натуральный", "бисексуальный", "фуривый", "жабий", "лесбийский", "трансгендерный", "квирный",
         "пансексуальный", "деми-сексуальный", "интерсексуальный", "асексуальный", "гетеросексуальный",
         "педерастический", "андрогинный", "гендерфлюидный", "полиаморный", "сквиртинговый", "фемдомный",
         "мазохистический", "садистический", "вояжерский", "зоофильский", "некрофильский", "ви-фи", "драговый",
         "русалочий", "киборговый", "роботичный", "мультипликаторский", "покемоновый", "фантастический",
         "цифровой", "свингерский", "веганский", "феминистский", "мизогинный", "сексворкерский", "полигамный",
         "садомазохистический", "киберпанковский", "косплейный", "фуррийский", "баблофильский",
         "антиконформистский", "татуировочный", "пирсинговый", "готический", "эмоциональный", "хиппи",
         "рейверский", "геймерский", "кинофильский", "книголюбский", "фотографический", "художественный",
         "музыкальный", "танцевальный", "актерский", "студенческий", "рабочий", "предпринимательский",
         "путешественнический", "фрилансовый", "интровертный", "экстравертный", "сномантский", "вегетарианский",
         "фрутарианский", "манифестантский", "революционерский", "антивакцинный", "донорский", "циничный",
         "оптимистический", "пессимистический", "реалистичный", "идеалистический", "утопистический",
         "рефлексивный", "латентный", "пограничный", "сталкерский", "абсентный", "квантовый", "стилобатный",
         "ситохимический", "гелиотипический", "аметабиозный", "авторитарный", "амфетаминовый", "триптический",
         "оптиматический", "прапигментный", "антопогонный", "рекурсионистический", "артистический",
         "якакашистический", "пеполнантский"]

def get_db_connection():
    if not hasattr(db_connections, 'connection'):
        db_connections.connection = sqlite3.connect('users_data.db')
    return db_connections.connection


def close_db_connection():
    if hasattr(db_connections, 'connection'):
        db_connections.connection.close()
        del db_connections.connection


bot = telebot.TeleBot('5997455790:AAHj53rKSK9HUK2ICdNh1qWWpbWSoyq2P48')


def generate_value(value_range):
    return random.uniform(value_range[0], value_range[1])


def generate_size():
    try:
        index = random.choices(range(len(percentages)), weights=percentages)[0]
        length = generate_value(length_ranges[index])
        width = generate_value(width_ranges[index])
        return length, width
    except Exception as ex:
        logger.error(str(ex))


@bot.message_handler(commands=['cock'])
def message_handler(message):
    try:
        user_id = message.from_user.id
        last_request_time = get_last_request_time(user_id)

        current_time = time.time()
        role = random.choice(roles)

        if last_request_time is None or current_time - last_request_time >= 12 * 60 * 60:
            length, width = generate_size()

            if message.from_user.username:
                nickname = message.from_user.username
            elif message.from_user.first_name and message.from_user.last_name:
                nickname = message.from_user.first_name + ' ' + message.from_user.last_name
            else:
                nickname = str(user_id)
            race = generate_pillar_image(int(width), int(length))
            save_last_request_time(user_id, current_time, round(length, 2), round(width, 2), nickname, role, race)
        else:
            length, width, role, race = get_last_request_size(user_id)
            race = generate_pillar_image(int(width), int(length), race)

        photo = open('image.png', 'rb')
        bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'У тебя {role} писюн\nДлина: {round(length, 2)} см\nДиаметр: {round(width, 2)} см\nРаса: {race}\nКачество сна: {random.randint(1,100)}%')
    except Exception as ex:
        logger.error(str(ex))


def get_last_request_time(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT last_request_time FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            return float(result[0])
        else:
            return None
    except Exception as ex:
        logger.error(str(ex))


def get_last_request_size(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('SELECT length, width, role, race FROM users WHERE id = ?', (user_id,))
        result = cursor.fetchone()

        return result[0], result[1], result[2], result[3]
    except Exception as ex:
        logger.error(str(ex))


def save_last_request_time(user_id, last_request_time, length, width, nickname, role, race):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute('INSERT OR REPLACE INTO users (id, last_request_time, length, width, nickname, role, race) VALUES (?, ?, ?, ?, ?, ?, ?)', (user_id, last_request_time, length, width, nickname, role, race))
        conn.commit()
    except Exception as ex:
        logger.error(str(ex))


@bot.message_handler(commands=['leaders'])
def get_leaderboard(message):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        one_day_ago_timestamp = time.time() - 24 * 60 * 60
        cursor.execute("SELECT nickname, length, width FROM users WHERE last_request_time > %s ORDER BY length DESC" %
                       (one_day_ago_timestamp,))
        results = cursor.fetchall()

        message_text = f'Leaderboards:'
        count = 0
        for i in results:
            if count < 15:
                message_text += f'\n{count+1}. {i[0]}: {i[1]} cm, {i[2]} cm'
            else:
                break
            count += 1
        bot.send_message(message.chat.id, text=message_text)
    except Exception as ex:
        logger.error(str(ex))


while True:
    try:
        bot.polling()
    except:
        time.sleep(5)
