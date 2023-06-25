import random
import telebot
from telebot import types
import sqlite3
import time
import threading
from PIL import Image, ImageDraw, ImageFont
import textwrap


db_connections = threading.local()

table_width = 600
table_height = 390
column_widths = [200, 200, 200]
header_height = 50
row_height = 30
font_size = 20

percentages = [3.3, 1.3, 7.4, 23.4, 35.8, 21.4, 6.9, 0.5]
length_ranges = [(7, 11), (11, 12), (12, 14), (14, 16.5), (16.5, 17.5), (17.5, 20), (20, 23), (23, 27)]
width_ranges = [(2.22, 2.41), (2.41, 2.8), (2.8, 3.18), (3.18, 3.58), (3.58, 3.97), (3.97, 4.39), (4.39, 4.77), (4.77, 6.33)]


def get_db_connection():
    if not hasattr(db_connections, 'connection'):
        db_connections.connection = sqlite3.connect('users_data.db')
    return db_connections.connection


def close_db_connection():
    if hasattr(db_connections, 'connection'):
        db_connections.connection.close()
        del db_connections.connection


bot = telebot.TeleBot('5997455790:AAElTvWZDe-ioKSddZAIec8RSG8GHHoA258')


def generate_value(value_range):
    return random.uniform(value_range[0], value_range[1])


def generate_size():
    index = random.choices(range(len(percentages)), weights=percentages)[0]
    length = generate_value(length_ranges[index])
    width = generate_value(width_ranges[index])
    return length, width


@bot.inline_handler(func=lambda query: True)
def inline_command_handler(query):
    user_id = query.from_user.id
    last_request_time = get_last_request_time(user_id)

    current_time = time.time()

    if last_request_time is None or current_time - last_request_time >= 24 * 60 * 60:
        length, width = generate_size()
        if query.from_user.username:
            nickname = query.from_user.username
        elif query.from_user.first_name and query.from_user.last_name:
            nickname = query.from_user.first_name + ' ' + query.from_user.last_name
        else:
            nickname = str(user_id)

        save_last_request_time(user_id, current_time, round(length), round(width), nickname)
    else:
        length, width = get_last_request_size(user_id)

    check_size_button = types.InlineQueryResultArticle(
        id=user_id,
        title='Проверить кок',
        input_message_content=types.InputTextMessageContent(
            message_text=f'My cock length: {round(length, 2)} сm, width: {round(width, 2)} cm'
        ),
    )

    bot.answer_inline_query(query.id, [check_size_button], cache_time=0)


def get_last_request_time(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT last_request_time FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()

    if result:
        return float(result[0])
    else:
        return None


def get_last_request_size(user_id, ):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT length, width FROM users WHERE id = ?', (user_id,))
    result = cursor.fetchone()

    return result[0], result[1]


def save_last_request_time(user_id, last_request_time, length, width, nickname):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT OR REPLACE INTO users (id, last_request_time, length, width, nickname) VALUES (?, ?, ?, ?, ?)', (user_id, last_request_time, length, width, nickname))
    conn.commit()


@bot.message_handler(commands=['leaders'])
def get_leaderboard(message):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT nickname, length, width FROM users ORDER BY length DESC")
    results = cursor.fetchall()

    image = Image.new("RGB", (table_width, table_height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Заголовки столбцов
    header_font = ImageFont.truetype("arial.ttf", font_size)
    header_text = ["Nickname", "Length", "Width"]
    header_x = 0
    for i, text in enumerate(header_text):
        header_width = column_widths[i]
        draw.rectangle(
            [(header_x, 0), (header_x + header_width, header_height)],
            fill=(200, 200, 200)
        )
        draw.text(
            (header_x + 5, 10),
            text,
            font=header_font,
            fill=(0, 0, 0)
        )
        header_x += header_width

    # Данные из базы данных
    data_font = ImageFont.truetype("arial.ttf", font_size)
    data_x = 0
    data_y = header_height
    for row in results:
        for i, cell in enumerate(row):
            cell_width = column_widths[i]
            draw.rectangle(
                [(data_x, data_y), (data_x + cell_width, data_y + row_height)],
                fill=(255, 255, 255)
            )
            text = str(cell)
            wrapped_text = textwrap.fill(text, width=12)
            draw.text(
                (data_x + 5, data_y + 10),
                wrapped_text,
                font=data_font,
                fill=(0, 0, 0)
            )
            data_x += cell_width
        data_x = 0
        data_y += row_height

    image.save("leaderboard.png")

    with open('leaderboard.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


bot.polling()

close_db_connection()
