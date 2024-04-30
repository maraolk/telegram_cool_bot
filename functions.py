from server import bot
import telebot
import csv
import random
import json



active_function={"game_cities": False,
                 "game_secrets": False,
                 "game_words": False,
                 "movie_year": False,
                 "movie_genre": False,
                 "movie_name": False
                 }

cities_list=[]

cities_list_played=[]

city_last=''

secrets_dict={}

secret_active={}

word = {}

word_active=''

subwords_active=[]



@bot.message_handler(commands=["start"])
def start(message):
    answer=f'{message.from_user.first_name}, привет! \n' \
           f'Давай начнём работу \n' \
           f'Для этого нужно ввести /menu'
    bot.send_message(chat_id=message.chat.id, text=answer)

@bot.message_handler(commands=["help"])
def help(message):
    answer=f"Я могу поиграть с тобой в такие игры как: \n"\
           f"1. Города \n"\
           f"2. Загадки \n"\
           f"3. Составь слова из слова \n"\
           f"Ещё я могу найти для тебя фильм по жанру, по названию и по году. \n"\
           f"Также ты можешь посмотреть картинки, которые я тебе отправлю или послушать музыку."
    bot.send_message(chat_id=message.chat.id, text=answer)

@bot.message_handler(commands=["movies"])
def movies(message):
    answer = 'Добро пожаловать в меню поиска фильма! \n' \
             'Я умею искать фильм по параметрам: \n' \
             '1. Название \n' \
             '2. Год \n' \
             '3. Жанр \n' \
             'Для того, чтобы начать выберите пункт меню!'
    bot.send_message(chat_id=message.chat.id, text=answer)
    movie_menu(message)

@bot.message_handler(commands=["commands"])
def commands(message):
    answer = f'Основные команды данного бота: \n' \
             '1. Для перехода к главному меню введите <i> /menu </i> \n' \
             '2. Для того, чтобы сыграть в игры введите <i> /games </i> \n' \
             '3. Для того, чтобы начать искать фильмы введите <i> /movies </i> \n' \
             '4. Для получения основной информации введите <i> /help </i> \n'
    bot.send_message(chat_id=message.chat.id, text=answer, parse_mode='html')

def movie_menu(message):
    active_function["movie_menu"]=False
    active_function["movie_genre"]=False
    active_function["movie_name"]=False
    movie_list=[["Поиск по названию"], ["Поиск по жанру", "Поиск по году"], ["Назад в главное меню"]]
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for movie in movie_list:
        markup.add(*movie)
    bot.send_message(chat_id=message.chat.id, text="Какой поиск тебя интересует?", reply_markup=markup)

def movie_year(message):
    if message.text == "Закончить" or message.text == "Назад в главное меню":
        movie_menu(message)
        return
    with open("data/movies.json", encoding='utf-8') as file:
        data=json.load(file)
    count_search=0
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Закончить")
    for i in range(len(data)):
        genre_arr=''
        if message.text == data[i]['year']:
            count_search +=1
            for j in range(len(data[i]['genre'])):
                genre_arr += data[i]['genre'][j]+'\t'
            answer = f'Название: <i>{data[i]["name"]}</i> \n' \
                     f'Жанры фильма: <i>{genre_arr}</i>'
            poster=open(data[i]['poster'], 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=poster, caption=answer, reply_markup=markup,
                           parse_mode='html')
            poster.close()
    if count_search == 0:
        answer= f'Фильмов с таким годом нет в моей базе \n'\
                f'Попробуйте поиск позже, когда я обновлю мою базу.'
        bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)

def movie_name(message):
    if message.text == "Закончить" or message.text == "Назад в главное меню":
        movie_menu(message)
        return
    with open("data/movies.json", encoding='utf-8') as file:
        data=json.load(file)
    count_search=0
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Закончить")
    for i in range(len(data)):
        genre_arr=''
        if message.text.lower() in data[i]['name'].lower():
            count_search +=1
            for j in range(len(data[i]['genre'])):
                genre_arr += data[i]['genre'][j]+'\t'
            answer = f'Название: <i>{data[i]["name"]}</i> \n' \
                     f'Жанры фильма: <i>{genre_arr}</i> \n' \
                     f'Год фильма: <i>{data[i]["year"]}</i>'
            poster=open(data[i]['poster'], 'rb')
            bot.send_photo(chat_id=message.chat.id, photo=poster, caption=answer, reply_markup=markup,
                           parse_mode='html')
            poster.close()
    if count_search == 0:
        answer= f'Фильмов с таким названием нет в моей базе \n'\
                f'Попробуйте поиск позже, когда я обновлю мою базу.'
        bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)

def movie_genre(message):
    if message.text == "Закончить" or message.text == "Назад в главное меню":
        movie_menu(message)
        return
    with open("data/movies.json", encoding='utf-8') as file:
        data=json.load(file)
    count_search=0
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("Закончить")
    for i in range(len(data)):
        genre_arr=data[i]["genre"]
        for genre in genre_arr:
            if message.text.lower() in genre.lower():
                count_search+=1
                answer = f'Название: <i>{data[i]["name"]}</i> \n' \
                     f'Год фильма: <i>{data[i]["year"]}</i>'
                poster = open(data[i]['poster'], 'rb')
                bot.send_photo(chat_id=message.chat.id, photo=poster, caption=answer, reply_markup=markup,
                           parse_mode='html')
                poster.close()
    if count_search == 0:
        answer= f'Фильмов с таким жанром нет в моей базе \n'\
                f'Попробуйте поиск позже, когда я обновлю мою базу.'
        bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)



def game_menu(message):
    active_function["game_cities"]=False
    active_function["game_secrets"]=False
    active_function["game_words"]=False
    game_list=[["Города", "Загадки"], ["Найди слова"], ["Назад в главное меню"]]
    markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for games in game_list:
        markup.add(*games)
    bot.send_message(chat_id=message.chat.id, text="Жду твоего решения", reply_markup=markup)

@bot.message_handler(commands=["games"])
def games(message):
    answer="Добро пожаловать в игровое меню! \n" \
           "1. Города \n" \
           "2. Загадки \n" \
           "3. Найди слова \n" \
           "4. Назад в главное меню\n"\
           "Для того, чтобы начать, выбери игру из меню"
    bot.send_message(chat_id=message.chat.id, text=answer)
    game_menu(message)



@bot.message_handler(commands=['menu'])
def menu(message):
    menu_list = [["Игры"],["Отправь картинку", "Отправь музыку"], ["Поиск фильма"]]
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for i in menu_list:
        markup.add(*i)
    answer="Добро пожаловать в крутого бота. Выбери, чем ты хочешь заняться.\n" \
           "1. Игры \n"\
           "2. Посмотреть картинки \n"\
           "3. Послушать музыку \n"\
           "4. Найти фильм \n"\
           "Жду твоего решения"
    bot.send_message(chat_id=message.chat.id, text=answer, reply_markup=markup)


# Заполнение массива с названием городов
def set_cities():
   with open("3 Day/city.csv", encoding='utf-8') as r_file:
       file_reader = csv.reader(r_file, delimiter=";") # Читаем файл
       for row in file_reader:
           cities_list.append(row[3])# Добавляем в массив названия городов

# Правила игры "Города"
def help_cities(message):
   global cities_list, cities_list_played # Используем наши переменные
   cities_list.clear()# Очищаем массив, чтобы города не дублировались
   cities_list_played.clear() # Очищаем массив, чтобы города не дублировались
   set_cities() # Запускаем функцию для чтения файла и добавления городов в массив
   answer = f'Приветствую в игре "Города" \n' \
            f'Давай для начала вспомним правила игры: \n' \
            f'Нужно называть города на последнюю букву \n' \
            f'Если последняя буквы Ы или Й, то называем на предпоследнюю \n' \
            f'Например: Москва (последняя буква А), значит следующим может быть Астрахань \n' \
            f'Попробуем сыграть?'
   markup = telebot.types.InlineKeyboardMarkup(row_width=2)# Создаём встроенную клавиатуру
   answer_yes = telebot.types.InlineKeyboardButton(text='Да', callback_data='cities_yes')# Создаём кнопку на продолжение игры
   answer_no = telebot.types.InlineKeyboardButton(text='Нет', callback_data='cities_no')# Создаём кнопку для окончания игры
   markup.add(answer_yes, answer_no)# Добавляем кнопки в клавиатуру
   bot.send_message(chat_id=message.chat.id,
                    text=answer,
                    reply_markup=markup)

# Процесс игры в города
def play_cities(message):
   global city_last, cities_list
   message.text = message.text.strip()
   if message.text in cities_list: # Если названный город есть в массиве возможных городов
       markup = telebot.types.InlineKeyboardMarkup(row_width=2)
       game_end = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='cities_no')
       last_char = telebot.types.InlineKeyboardButton(text='На какую букву', callback_data='last_char')
       markup.add(last_char, game_end)
       # cities_list.remove(message.text)# Удаляем из массива городов названный пользователем город
       check_last_city = False  # Проверка на правильность введённого города
       check_played_city = False  # Проверка на ранее сыгранное слово

       if city_last == '':
           check_last_city = True
       elif message.text[0].lower() == city_last[-1]: # Если первая буква города равна последней букве последнего названного города
           check_last_city = True

       if message.text not in cities_list_played:
           check_played_city = True

       if message.text[-1] == 'ь' or message.text[-1] == 'ы' or message.text[-1] == 'й':
           message.text = message.text[:-1]

       if message.text not in cities_list_played and check_last_city and check_played_city:
           cities_list_played.append(message.text)  # Добавляем названный город в массив сыгранных городов
           for city in cities_list:
               if city[0].lower() == message.text[-1] and city not in cities_list_played: # Если первая буква найденного города равна последней введенного
                   answer = city # Ответ бота - найденный город
                   cities_list_played.append(city) # Добавляем названный город в массив сыгранных городов
                   # cities_list.remove(city) # Удаляем из массива возможных городов
                   if city[-1] == 'ь' or city[-1] == 'ы' or city[-1] == 'й':
                       city_last = city[:-1] # Последний город равен ответу бота
                   else:
                       city_last = city
                   bot.send_message(chat_id=message.chat.id,
                                    text=answer,
                                    reply_markup=markup)
                   break
       else:
           answer = f'Такой город уже называли'
           bot.send_message(chat_id=message.chat.id,
                            text=answer,
                            reply_markup=markup)
   else:
       answer = f'Такого города не существует \n' \
                f'Попробуй ещё раз'
       bot.send_message(chat_id=message.chat.id,
                        text=answer)


def set_secrets():
   with open("3 Day/secret.csv", encoding='utf-8') as r_file:
       file_reader = csv.reader(r_file, delimiter=";")
       for row in file_reader:
           row[0] = row[0].replace(r'\n', '\n')
           secrets_dict[row[0]] = row[1]

# Правила игры "Загадки"
def help_secret(message):
   global secrets_dict, secret_active
   secrets_dict.clear() # Очищаем словарь загадок
   secret_active.clear()# Очищаем словарь текущей загадки
   set_secrets() # Читаем файл с загадками
   answer = f'Приветствую в моей игре "Загадки" \n' \
            f'Правила очень простые \n' \
            f'Я задаю тебе загадку, а тебе нужно предлагать ответы \n' \
            f'Удачи!'
   markup = telebot.types.InlineKeyboardMarkup(row_width=2)
   secret_start = telebot.types.InlineKeyboardButton(text='Начать', callback_data='secret_yes')
   secret_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='secret_no')
   markup.add(secret_start, secret_stop)
   bot.send_message(chat_id=message.chat.id,
                    text=answer,
                    reply_markup=markup)


# Загадываем загадку пользователю
def send_secret(message):
   secret_active.clear() # Очищаем словарь текущей загадки
   if len(secrets_dict) != 0:
       secret_sends, answer_secret = random.choice(list(secrets_dict.items())) # Выбираем рандомную загадку
       secrets_dict.pop(secret_sends) # Удаляем загадку из словаря загадок
       secret_active[secret_sends] = answer_secret # Устанавливаем текущую загадку и ответ на неё
       bot.send_message(chat_id=message.chat.id,
                        text=f'<b>Моя загадка:</b> \n'
                             f'{secret_sends}',
                        parse_mode='html')
   else:
       answer = 'У меня закончились загадки \n' \
                'Давай попробуем в следующий раз :)'
       bot.send_message(chat_id=message.chat.id,
                        text=answer)
       game_menu(message)# Возвращаемся в игровое меню

# Процесс игры в Загадки
def play_secret(message):
   sec = secret_active.keys()
   answer_secret = ''
   for i in sec:
       answer_secret = secret_active.get(i)
       answer_secret = answer_secret.lower()
   if message.text.strip().lower() == answer_secret:
       markup = telebot.types.InlineKeyboardMarkup(row_width=2)
       secret_next = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='secret_yes')
       secret_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='secret_no')
       markup.add(secret_next, secret_stop)
       bot.send_message(chat_id=message.chat.id,
                        text='Молодец!',
                        reply_markup=markup)
   else:
       markup = telebot.types.InlineKeyboardMarkup(row_width=2)
       secret_answer = telebot.types.InlineKeyboardButton(text='Ответ', callback_data='secret_answer')
       secret_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='secret_no')
       markup.add(secret_answer, secret_stop)
       bot.send_message(chat_id=message.chat.id,
                        text='Неверный ответ! \n'
                             'Подумай ещё',
                        reply_markup=markup)

# Наполняем массивы словами
def set_word():
    global word, word_active
    with open("4 Day/words.json", encoding='utf-8') as file:
        data = json.load(file) # Читаем файл

    for i in range(len(data)):
        word[data[i]["word"]] = data[i]["subwords"] # Добавляем новые элементы в словарь

# Правила игры "Найди слова"
def help_words(message):
    global word, subwords_active
    word.clear() # Очищаем словарь всех слов
    subwords_active.clear() # Очищаем массив всех подслов загаданного слова
    set_word() # Читаем файл и заполняем словари
    answer = f'Приветствую в моей игре "Найди слова" \n' \
             f'Правила очень простые \n' \
             f'Я задаю тебе слово, \n' \
             f'А тебе нужно найти все слова, которые можно из него составить \n' \
             f'Удачи!'
    markup = telebot.types.InlineKeyboardMarkup(row_width=2)
    word_start = telebot.types.InlineKeyboardButton(text='Начать', callback_data='word_yes')
    word_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='word_no')
    markup.add(word_start, word_stop)
    bot.send_message(chat_id=message.chat.id,
                     text=answer,
                     reply_markup=markup)

# Загадываем слово
def send_word(message):
    global word_active, subwords_active
    word_active = '' # Очищаем загаданное слово
    subwords_active.clear()  # Очищаем словарь текущих подслов
    if len(word) != 0: # Если ещё не все слова были сыграны
        word_active, subwords_active = random.choice(list(word.items()))  # Выбираем рандомное слово
        word.pop(word_active)  # Удаляем слово из словаря
        bot.send_message(chat_id=message.chat.id,
                         text=f'<b>Я загадываю слово:</b> \n'
                              f'{word_active} \n'
                              f'Тебе нужно будет назвать: {len(subwords_active)} слов',
                         parse_mode='html')
    else:
        answer = 'У меня закончились слова \n' \
                 'Давай попробуем в следующий раз :)'
        bot.send_message(chat_id=message.chat.id,
                         text=answer)
        game_menu(message) # Возвращаемся в игровое меню


# Процесс игры в "Найди слова"
def play_word(message):
    global subwords_active
    # Если пользователь ввёл правильное слово и оно является последним
    if message.text.strip().lower() in subwords_active and len(subwords_active) == 1:
        subwords_active.remove(message.text.strip().lower())  # Удаляем подслово из массива
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        word_cont = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='word_yes')
        word_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='word_no')
        markup.add(word_cont, word_stop)
        answer = f'Ты отгадал все слова, которые можно составить из слова {word_active} \n' \
                 f'Хочешь продолжить?'
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

    # Если пользователь угадал слово и оно не последнее
    elif message.text.strip().lower() in subwords_active and len(subwords_active) > 1:
        subwords_active.remove(message.text.strip().lower())
        markup = telebot.types.InlineKeyboardMarkup(row_width=1)
        word_help_user = telebot.types.InlineKeyboardButton(text='Подсказка', callback_data='word_help')
        markup.add(word_help_user)
        answer = f'Такое слово присутствует \n' \
                 f'Осталось угадать: {len(subwords_active)} слов'
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)

    # Если пользователь не угадал слово
    elif message.text.strip().lower() not in subwords_active:
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        word_help_user = telebot.types.InlineKeyboardButton(text='Подсказка', callback_data='word_help')
        word_finish=telebot.types.InlineKeyboardButton(text='Закончить', callback_data='finish_words')
        markup.add(word_help_user, word_finish)
        answer = f'Такого слова нет \n' \
                 f'Попробуй ещё раз'
        bot.send_message(chat_id=message.chat.id,
                         text=answer,
                         reply_markup=markup)



# Обработка встроенных кнопок в сообщение
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Играем в города
    if call.data == 'cities_yes':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Жду от тебя название первого города!')
        active_function["game_cities"] = True

    # На какую букву называем город
    elif call.data == 'last_char':
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'{city_last[-1].upper()}')

    # Отказываемся играть в города
    elif call.data == 'cities_no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Буду ждать следующей игры!')
        games(call.message)
        active_function["game_cities"] = False

 # Играем в загадки
    elif call.data == 'secret_yes':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        active_function["game_secrets"] = True
        send_secret(call.message)

    # Получить ответ на загадку
    elif call.data == 'secret_answer':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        sec = secret_active.keys()
        answer = ''
        for i in sec:
            answer = secret_active.get(i)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f'Ответ: {answer} \n'
                              f'Запомни ответ на загадку!')
        send_secret(call.message)

    # Заканчиваем играть в загадки
    elif call.data == 'secret_no':
        bot.delete_message(chat_id=call.message.chat.id,
                           message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id,
                         text='Буду ждать следующей игры!')
        games(call.message)
        active_function["game_secrets"] = False

    elif call.data == "word_yes":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        active_function["game_words"]=True
        send_word(call.message)
    elif call.data == "word_no" or call.data == "finish_words":
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)
        bot.send_message(chat_id=call.message.chat.id, text="Буду ждать следующей игры")
        active_function["game_words"] = False
        games(call.message)

# Помощь в "Найди слова"
    elif call.data == 'word_help':
        if len(subwords_active) != 1:
            random_index = random.randrange(len(subwords_active))
            answer = subwords_active[random_index]
            subwords_active.remove(answer)
            bot.send_message(chat_id=call.message.chat.id,
                             text=f'Есть такое слово: {answer} \n'
                                  f'Осталось слов: {len(subwords_active)} слов')

        elif len(subwords_active) == 1:
            random_index = random.randrange(len(subwords_active))
            answer = subwords_active[random_index]
            subwords_active.remove(answer)
            markup = telebot.types.InlineKeyboardMarkup(row_width=2)
            word_cont = telebot.types.InlineKeyboardButton(text='Продолжить', callback_data='word_yes')
            word_stop = telebot.types.InlineKeyboardButton(text='Закончить', callback_data='word_no')
            markup.add(word_cont, word_stop)
            bot.send_message(chat_id=call.message.chat.id,
                             text=f'Это последнее слово: {answer}',
                             reply_markup=markup)

@bot.message_handler(commands=["stop"])
def stop(message):
    bot.send_message(chat_id=message.chat.id, text="Я заканчиваю свою работу, пока!")

@bot.message_handler(content_types=["text"])
def action(message):
    if message.text == "Как дела?":
        bot.send_message(chat_id=message.chat.id, text="Всё хорошо")
    elif message.text == "Как тебя зовут?":
        bot.send_message(chat_id=message.chat.id, text="Меня зовут крутой бот.")
    elif message.text == "Сколько тебе лет?":
        bot.send_message(chat_id=message.chat.id, text="Мне 14 лет.")
    elif message.text == "Из какого ты города?":
        bot.send_message(chat_id=message.chat.id, text="Я из Москвы.")
    elif message.text == "Как зовут твоего разработчика?":
        bot.send_message(chat_id=message.chat.id, text="Моего разработчика зовут Арина.")
    elif message.text == "Отправь картинку":
        text_1='2 Day/img/'+str(random.randint(1,5))+".jpg"
        image=open(text_1, 'rb')
        bot.send_photo(chat_id=message.chat.id, photo=image, caption="Я нашёл картинку")
        image.close()
    elif message.text == "Отправь музыку":
        text_2 ='2 Day/mp3/' + str(random.randint(2, 3)) +".mp3"
        music=open(text_2, 'rb')
        bot.send_audio(chat_id=message.chat.id, audio=music, caption="Я нашёл вот такой трек")
        music.close()
    elif message.text == "Игры":
        games(message)
    elif message.text=="Города":
        help_cities(message)
    elif active_function["game_cities"]:
        play_cities(message)
    elif message.text == "Загадки":
        help_secret(message)
    elif active_function["game_secrets"]:
        play_secret(message)
    elif message.text=="Найди слова":
        help_words(message)
    elif active_function["game_words"]:
        play_word(message)
    elif message.text=="Поиск фильма":
        movie_menu(message)
    elif message.text=="Поиск по году":
        active_function["movie_year"]=True
        active_function["movie_name"]=False
        active_function["movie_name"]=False
        bot.send_message(chat_id=message.chat.id, text="Введи год фильмов, которые ты хочешь найти \n"
                                                       "Например: 2022")
    elif active_function["movie_year"]:
        movie_year(message)
    elif message.text=="Поиск по названию":
        active_function["movie_year"]=False
        active_function["movie_name"]=True
        active_function["movie_genre"]=False
        bot.send_message(chat_id=message.chat.id, text="Введи название фильма, который ты хочешь найти \n"
                                                       "Например: Король лев")
    elif active_function["movie_name"]:
        movie_name(message)
    elif message.text == "Назад в главное меню":
        menu(message)
    elif message.text=="Поиск по жанру":
        active_function["movie_year"]=False
        active_function["movie_name"]=False
        active_function["movie_genre"]=True
        bot.send_message(chat_id=message.chat.id, text="Введи жанр фильма, который ты хочешь найти \n"
                                                       "Например: Фантастика")
    elif active_function["movie_genre"]:
        movie_genre(message)


