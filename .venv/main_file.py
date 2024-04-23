import telebot
from telebot import types
from PIL import Image
import io
import sqlite3
import time
import os
import hashlib

result_of_var = 0
task_num = 0
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
    'Кинематика': ['Скорость', 'Ускорение', 'Равномерное и равноускоренное прямолинейное движение', 'Прямолинейное движение и движение по окружности'],
    'Динамика': ['Закон Ньютона', 'Равнодействующая', 'Закон всемирного тяготения', 'Сила трения', 'Давление', 'Сила Архимеда'],
    'Законы сохранения': ['Закон сохранения импульса', 'Законы изменения и сохранения энергии'],
    'Термодинамика': ['Закон Гука', 'Закон Ампера', 'Закон Фарадея', 'Уравнение состояния идеального газа', 'Изопроцессы',
                       'Процессы нагревания, плавления, парообразования, горения', 'Первое начало термодинамики',
                       'Тепловые машины и их циклы', 'КПД'],
    'Электродинамика': ['Электрический заряд', 'Закон сохранения заряда', 'Закон Кулона', 'Напряженность и потенциал электростатического поля',
                        'Конденсатор', 'Электрический ток', 'Сила тока', 'Сопротивление', 'Закон Ома', 'Закон Джоуля-Ленца',
                        'Магнитное поле', 'Сила Лоренца', 'Сила Ампера', 'Электромагнитная индукция', 'Правило Ленца',
                        'Катушка индуктивности и явление самоиндукции', 'Электромагнитные колебания и волны'],
    'Оптика': ['Геометрическая оптика', 'Отражение и преломление света', 'Тень и полутень', 'Виды и свойства линз',
               'Построение изображения в линзах', 'Давление света'],
    'Кванотвая физика': ['Энергетические переходы и СТО', 'Импульс и энергия фотона', 'Фотоэффект', 'Уравнение Эйнштейна для фотоэффекта',
                'Строение атома', 'Ядерные реакции', 'Законы радиоактивного распада']
}


bot_info = {
    "Цель и задачи бота": "Приветствуем тебя в боте для подготовки к экзамену ЕГЭ по физике! Наш бот создан с целью помочь тебе эффективно подготовиться к сдаче экзамена, предоставив удобный и доступный инструмент для изучения ключевых тем и заданий по физике.",
    "Функциональность бота": "Бот имеет разнообразные и полезные функции направленные на подготовку к ЕГЭ по физике. Здесь вы сможете полностью погрузиться в процесс подготовки.",
    "Структура контента": "При старте бота рекомендуется сразу нажать раздел о боте. В нем вы найдете всю полезную информацию об управлении ботом. Остальные кнопки говорят сами за себя!",
    "Методы обучения": "Наш бот предлагает разнообразные методы обучения, направленные на эффективное усвоение теоретического материала и закрепление полученных знаний через решение задач.",
    "Инструкции": "При нажатии на каждый раздел бот предоставит вам полную инструкцию о том, как действовать дальше. Читайте внимательно!",
    "Правила использования": "Используйте бот так, как пожелаете нужным и полезным!",
    "О разработчике": "Меня зовут Максим и я учусь в 10-ом классе. На создание данного бота меня вдохновила ОЧЕНЬ(нет) воодушевляющая мысль о сдаче ЕГЭ по физике через год.",
    "Помощь и ресурсы": "Все ресурсы я брал из открытых источников. Вы также можете у меня их копировать.",
    "Авторские права": "Без использования авторских прав. Код и материалы принадлежат Человечеству и мне :)",
    "Обновления": "Я постараюсь сохранить поддержку версий бота и добавлять новые материалы."
}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Создаем и отображаем клавиатуру с кнопками
    markup = types.ReplyKeyboardMarkup(row_width=2)
    itembtn1 = types.KeyboardButton('Теория к заданиям')
    itembtn2 = types.KeyboardButton('Составить случайный вариант')
    itembtn3 = types.KeyboardButton('Задания определенного типа')
    itembtn4 = types.KeyboardButton('Об управлении ботом')
    markup.add(itembtn1, itembtn2, itembtn3, itembtn4)

    bot.reply_to(message, "Привет! Я бот для подготовки к ЕГЭ по физике. Выбери одну из опций:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == 'Составить случайный вариант')
def random_variant(message):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    # Получаем случайные задания из базы данных
    cursor.execute("SELECT num, quest, answer FROM tasks")
    tasks = cursor.fetchall()
    lst = []
    for i in range(1, 27):
        lst.append(list(set(filter(lambda x: x[0] == i, tasks)))[0])

    # Создаем список заданий для последовательной обработки
    task_list = list(lst)

    # Проверяем, есть ли задания
    if len(task_list) > 0:
        # Получаем первое задание
        task = task_list[0]

        # Удаляем первое задание из списка
        del task_list[0]

        # Получаем путь к картинке задания
        image_path = 'images/' + task[1] + '.png'

        # Открываем картинку с помощью модуля PIL
        image = Image.open(image_path)

        # Получаем размеры картинки
        width, height = image.size

        # Вычисляем новые размеры с соотношением сторон 2:1
        new_width = width
        new_height = int(new_width / 2)

        # Создаем новое изображение белого цвета с новыми размерами
        new_image = Image.new("RGB", (new_width, new_height), "white")

        # Вычисляем вертикальное смещение
        offset = int((new_height - height) / 2)

        # Вставляем исходное изображение на новое смещенное изображение
        new_image.paste(image, (0, offset))

        # Сохраняем новое изображение временно
        temp_image_path = "temp_image.png"
        new_image.save(temp_image_path)

        # Отправляем фото задания
        with open(temp_image_path, 'rb') as image_file:
            bot.send_photo(chat_id=message.chat.id, photo=image_file)

        # Сохраняем правильный ответ для проверки
        correct_answer = task[2]

        # Регистрируем обработчик для ожидания ответа пользователя
        bot.register_next_step_handler(message, check_answer1, task_list, task[1], correct_answer)

        # Удаляем временное изображение
        os.remove(temp_image_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Задания закончились')


def handle_message(message):
    bot.send_message(chat_id=message.chat.id, text='Введите номер задания, которое хотите проработать:')
    while model == 0:
        bot.register_next_step_handler(message, process_text)


my_ans = '0'
model = 0


def process_text(message):
    global model
    model = message.text


@bot.message_handler(func=lambda message: message.text == 'Задания определенного типа')
def tasks_of_type(message):
    # Устанавливаем соединение с базой данных
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()

    handle_message(message)
    # Получаем случайные задания из базы данных
    cursor.execute("SELECT num, quest, answer FROM tasks")
    tasks = cursor.fetchall()
    print(tasks)
    lst = []
    for i in range(1, 27):
        lst = list(filter(lambda x: str(x[0]) == model, tasks))
    print(lst)

    # Создаем список заданий для последовательной обработки
    task_list = lst

    # Проверяем, есть ли задания
    if len(task_list) > 0:
        # Получаем первое задание
        task = task_list[0]

        # Удаляем первое задание из списка
        del task_list[0]

        # Получаем путь к картинке задания
        image_path = 'images/' + task[1] + '.png'

        # Открываем картинку с помощью модуля PIL
        image = Image.open(image_path)

        # Получаем размеры картинки
        width, height = image.size

        # Вычисляем новые размеры с соотношением сторон 2:1
        new_width = width
        new_height = int(new_width / 2)

        # Создаем новое изображение белого цвета с новыми размерами
        new_image = Image.new("RGB", (new_width, new_height), "white")

        # Вычисляем вертикальное смещение
        offset = int((new_height - height) / 2)

        # Вставляем исходное изображение на новое смещенное изображение
        new_image.paste(image, (0, offset))

        # Сохраняем новое изображение временно
        temp_image_path = "temp_image.png"
        new_image.save(temp_image_path)

        # Отправляем фото задания
        with open(temp_image_path, 'rb') as image_file:
            bot.send_photo(chat_id=message.chat.id, photo=image_file)

        # Сохраняем правильный ответ для проверки
        correct_answer = task[2]
        print(task_list, task[1], correct_answer)
        # Регистрируем обработчик для ожидания ответа пользователя
        bot.register_next_step_handler(message, check_answer1, task_list, task[1], correct_answer)
        # Удаляем временное изображение
        os.remove(temp_image_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Задания закончились')


def check_answer1(message, task_list, image_path, correct_answer):
    global result_of_var
    # Сравниваем ответ пользователя с полем answer
    if message.text == correct_answer:
        bot.send_message(chat_id=message.chat.id, text='Правильно!')
        result_of_var += 1
    else:
        bot.send_message(chat_id=message.chat.id, text='Неправильно! Посмотри авторское решение!')
        image_path1 = 'images/' + image_path[:-1] + 's.png'

        # Открываем картинку с помощью модуля PIL
        image = Image.open(image_path1)

        # Получаем размеры картинки
        width, height = image.size

        # Вычисляем новые размеры с соотношением сторон 2:1
        new_width = width
        new_height = int(new_width / 2)

        # Создаем новое изображение белого цвета с новыми размерами
        new_image = Image.new("RGB", (new_width, new_height), "white")

        # Вычисляем вертикальное смещение
        offset = int((new_height - height) / 2)

        # Вставляем исходное изображение на новое смещенное изображение
        new_image.paste(image, (0, offset))

        # Сохраняем новое изображение временно
        temp_image_path = "temp_image.png"
        new_image.save(temp_image_path)

        # Отправляем фото задания
        with open(temp_image_path, 'rb') as image_file:
            bot.send_photo(chat_id=message.chat.id, photo=image_file)

    # Проверяем, есть ли еще задания в списке
    if len(task_list) > 0:
        # Получаем следующее задание из списка
        next_task = task_list[0]

        # Удаляем задание из списка
        del task_list[0]
        # Получаем путь к картинке задания
        next_image_path = 'images/' + next_task[1] + '.png'

        # Открываем следующую картинку с помощью модуля PIL
        next_image = Image.open(next_image_path)

        # Получаем размеры следующей картинки
        width, height = next_image.size

        # Вычисляем новые размеры следующей картинки с соотношением сторон 2:1
        new_width = width
        new_height = int(new_width / 2)

        # Создаем новое изображение белого цвета с новыми размерами
        new_image = Image.new("RGB", (new_width, new_height), "white")

        # Вычисляем вертикальное смещение
        offset = int((new_height - height) / 2)

        # Вставляем следующую картинку на новое смещенное изображение
        new_image.paste(next_image, (0, offset))
        # Сохраняем следующее изображение временно
        temp_image_path = "temp_image.png"
        new_image.save(temp_image_path)

        # Отправляем фото следующего задания
        with open(temp_image_path, 'rb') as image_file:
            bot.send_message(chat_id=message.chat.id,
                             text='Следующее задание:')
            bot.send_photo(chat_id=message.chat.id, photo=image_file)

        # Сохраняем правильный ответ следующего задания для проверки
        next_correct_answer = next_task[2]

        # Регистрируем обработчик для ожидания ответа пользователя
        bot.register_next_step_handler(message, check_answer1, task_list, next_task[1], next_correct_answer)

        # Удаляем временное изображение
        os.remove(temp_image_path)
    else:
        bot.send_message(chat_id=message.chat.id, text='Задания закончились, ваш результат: ' + str(round(result_of_var / 25 * 100, 2)) + '%')


@bot.message_handler(func=lambda message: message.text == 'Об управлении ботом')
def about_bot(message):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    for key in bot_info.keys():
        keyboard.add(types.InlineKeyboardButton(text=key, callback_data=key))
    bot.send_message(message.chat.id, "Выберите команду:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data in bot_info.keys())
def command_handler(call):
    command = call.data
    bot.send_message(call.message.chat.id, bot_info[command])


# Обрабатываем нажатия на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Отправляем текст из базы данных, соответствующий нажатой кнопке
    bot.send_message(call.message.chat.id, call.data)


# Важно: не забудьте закрыть соединение с базой данных после использования бота
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
