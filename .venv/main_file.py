import telebot
from telebot import types

import sqlite3


def get_data_by_name(name):
    # Подключаемся к базе данных
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # Выполняем SQL-запрос для получения данных по имени
    cursor.execute("SELECT data FROM theory WHERE name=?", (name,))
    data = cursor.fetchone()

    # Закрываем соединение с базой данных
    cursor.close()
    conn.close()

    # Возвращаем результат
    if data:
        return data[0]
    else:
        return None

# Замените 'TOKEN' на ваш токен доступа
bot = telebot.TeleBot('7089398283:AAFDLKbuqH-2ai324BokTZWzeD-12ObwvDc')

# Подразделы физики
subtopics = {
    'kinematics': ['Скорость', 'Ускорение', 'Равномерное и равноускоренное прямолинейное движение', 'Прямолинейное движение и движение по окружности'],
    'dynamics': ['Закон Ньютона', 'Равнодействующая', 'Закон всемирного тяготения', 'Сила трения', 'Давление', 'Сила Архимеда'],
    'conservation': ['Закон сохранения импульса', 'Законы изменения и сохранения энергии'],
    'thermodynamics': ['Закон Гука', 'Закон Ампера', 'Закон Фарадея', 'Уравнение состояния идеального газа', 'Изопроцессы',
                       'Процессы нагревания, плавления, парообразования, горения', 'Первое начало термодинамики',
                       'Тепловые машины и их циклы', 'КПД'],
    'electrodynamics': ['Электрический заряд', 'Закон сохранения заряда', 'Закон Кулона', 'Напряженность и потенциал электростатического поля',
                        'Конденсатор', 'Электрический ток', 'Сила тока', 'Сопротивление', 'Закон Ома', 'Закон Джоуля-Ленца',
                        'Магнитное поле', 'Сила Лоренца', 'Сила Ампера', 'Электромагнитная индукция', 'Правило Ленца',
                        'Катушка индуктивности и явление самоиндукции', 'Электромагнитные колебания и волны'],
    'optics': ['Геометрическая оптика', 'Отражение и преломление света', 'Тень и полутень', 'Виды и свойства линз',
               'Построение изображения в линзах', 'Давление света'],
    'quantum': ['Энергетические переходы и СТО', 'Импульс и энергия фотона', 'Фотоэффект', 'Уравнение Эйнштейна для фотоэффекта',
                'Строение атома', 'Ядерные реакции', 'Законы радиоактивного распада']
}

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем и отображаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Теория к заданиям')
    itembtn2 = types.KeyboardButton('Составить случайный вариант')
    itembtn3 = types.KeyboardButton('Составить вариант самому')
    itembtn4 = types.KeyboardButton('Об управлении ботом')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.reply_to(message, "Привет! Я бот для подготовки к ЕГЭ по физике. Выбери одну из опций:", reply_markup=markup)

# Обработчик нажатия на кнопку 'Теория к заданиям'
@bot.message_handler(func=lambda message: message.text == 'Теория к заданиям')
def send_subtopics(message):
    # Создаем и отображаем клавиатуру с подразделами физики
    markup = types.InlineKeyboardMarkup(row_width=2)
    for subtopic in subtopics:
        button = types.InlineKeyboardButton(subtopic, callback_data=subtopic)
        markup.add(button)

    bot.reply_to(message, "Выбери одну из областей физики:", reply_markup=markup)


# Обработчик нажатия на подраздел физики
@bot.callback_query_handler(func=lambda call: call.data in subtopics)
def send_topic_list(call):
    topic_list = subtopics[call.data]
    # Проверяем, есть ли список подтем для выбранного подраздела
    if topic_list:
        topic_text = "Подтемы для раздела {}: \n\n".format(call.data)
        markup = types.InlineKeyboardMarkup(row_width=1)
        for i, topic in enumerate(topic_list):
            button = types.InlineKeyboardButton(topic, callback_data=call.data + ' ' + str(i))
            markup.add(button)

        bot.send_message(call.message.chat.id, topic_text, reply_markup=markup)
    else:
        bot.send_message(call.message.chat.id, "Для раздела {} нет доступных подтем.".format(call.data))



# Обработчик нажатия на кнопку
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    top, ind = call.data.split()
    text = get_data_by_name(subtopics[top][int(ind)])
    bot.send_message(call.message.chat.id, text)


bot.polling()
