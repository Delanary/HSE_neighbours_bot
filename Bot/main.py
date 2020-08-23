import datetime
import sqlite3

import telebot
from telebot import types

log = open('log.txt', 'a')
f = open('token', 'r')
token = f.read().strip()
print(token)
f.close()
telebot.apihelper.proxy = {'https': 'socks5://repkach:pinkodch1488@socks.repka.ch:1080',
                           'http': 'socks5://repkach:pinkodch1488@socks.repka.ch:1080'}


def gen_username(message):
    account_name = ''
    if message.from_user.username:
        account_name += ' ' + message.from_user.username
    else:
        account_name += 'NONE'
    if message.from_user.first_name:
        account_name += ' ' + message.from_user.first_name
    if message.from_user.last_name:
        account_name += ' ' + message.from_user.last_name
    return account_name


DEBUG = False
admins = [378466098, 151497226, 251474581]
admins_chat_id = [-1001312819916]
hostels_dict = {'Переяславская, д. 50': "1", 'Электродная, д. 1': '2',
                'Энергетическая, д. 10': '3', 'Студенческая, д. 33/1': '4',
                'Кибальчича, д. 7': '5', 'Комсомольская, д. 1': '6',
                'Саратовский проезд, д. 5, к. 2': '7 1',
                'Саратовский проезд, д. 7, к. 3': '7 2',
                'Маковского, д. 2': '8', 'Цимлянская, 5': '9',
                'Михайлова, д. 34': '10',
                'Люблинская, д.56/2': '11',
                'Дениса Давыдова, д. 1': '12 1',
                'Дениса Давыдова, д. 3': '12 2',
                'Дениса Давыдова, д. 9': '12 3'
                }
hostels_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
hostels_markup.row("Переяславская, д. 50", 'Электродная, д. 1', )
hostels_markup.row('Энергетическая, д. 10', "Студенческая, д. 33/1", )
hostels_markup.row('Кибальчича, д. 7', 'Комсомольская, д. 1')
hostels_markup.row('Саратовский проезд, д. 5, к. 2', 'Саратовский проезд, д. 7, к. 3')
hostels_markup.row('Маковского, д. 2', 'Цимлянская, 5', )
hostels_markup.row('Михайлова, д. 34', 'Люблинская, д.56/2', )
hostels_markup.row('Дениса Давыдова, д. 1', 'Дениса Давыдова, д. 3')
hostels_markup.row('Дениса Давыдова, д. 9')
yesno_markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
yesno_markup.row("Да", "Нет")
default_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
default_markup.row('/know', '/from', '/vk')
NONE_markup = telebot.types.ReplyKeyboardRemove()
know_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
know_markup.row('по комнате', 'по квартире')
bot = telebot.TeleBot(token)
NONE_command = 'NONE NONE'
NONE_place = 'NaP'
NONE_user = -1
NONE_vk = 'User haven\'t specified vk url'
NONE_message = 'Empty message'
NONE_time = datetime.datetime(2000, 10, 1, 0, 1, 1, 1)
print(NONE_time)
error_ans = 'Я вас не понял, /stop, чтобы прекратить текущее взаимодействие.'
force_reply = types.ForceReply(selective=False)


def commit_previous_command(user_id, command):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET previous_command = ? WHERE account_id = ?"
              , [command, user_id])
    conn.commit()


def user_update(message):
    conn = sqlite3.connect('users.db')
    account_name = gen_username(message)
    account_id = message.from_user.id
    c = conn.cursor()
    c.execute("UPDATE users SET account_name = ? WHERE account_id = ?"
              , [account_name, account_id])
    conn.commit()


def is_user_exists(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE account_id = ?", [user_id])
    if len(c.fetchall()) > 0:
        conn.commit()
        return True
    else:
        conn.commit()
        return False


def change_user_info(column_name, value, user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    print(column_name, value, user_id)
    c.execute("UPDATE users SET {} = ? WHERE account_id = ? ".format(column_name)
              , (value, user_id))
    conn.commit()


def first_check(message):
    if True:
        account_name = gen_username(message)
        account_id = message.from_user.id
        if not is_user_exists(account_id):
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            print(NONE_time)
            c.execute("""
                        INSERT INTO users VALUES (?,?,?,?,?,?,?,?) 
                    """, (
                account_name, account_id, NONE_place, NONE_place, NONE_place, NONE_command, str(NONE_time), NONE_vk))
            conn.commit()


def send_message(user_id, text, reply_markup=NONE_markup):
    global bot

    def lol():
        try:
            for i in range(len(text) // 2000 + 1):
                bot.send_message(user_id, text[i * 2000: (i + 1) * 2000],
                                 reply_markup=reply_markup, parse_mode='html')
        except Exception as e:
            File = open('log.txt', 'a')
            print(e, datetime.datetime.now(), file=File)
            File.close()

    print(user_id, text)
    if text == '':
        text += NONE_message
    if DEBUG:
        if (user_id in admins) or (user_id in admins_chat_id):
            lol()
    elif user_id != NONE_user:
        lol()
    else:
        temp = open('log.txt', 'a')
        print('Somebody send %s to a none user' % text, file=f)
        temp.close()


def get_previous_command(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT previous_command FROM users WHERE account_id = ?"
              , [user_id])
    prev_command = c.fetchone()[0]
    conn.commit()
    return prev_command


def white_list(message):
    if message.from_user.id not in [151497226, 378466098]:
        return False
    else:
        return True


def admin_send_message(admin_chat, message):
    send_message(admin_chat,
                 '@%s по id %s сказал: %s' % (message.from_user.username, message.from_user.id, message.text), )


def admin_log_message(admin_chat, text):
    send_message(admin_chat, text)


def get_user_place(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT hostel,apartments,room FROM users WHERE account_id = ?", [user_id])
    user = c.fetchone()
    conn.commit()
    return user


def get_user_last_change(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT last_change FROM users WHERE account_id = ?", [user_id])

    user = c.fetchone()
    conn.commit()
    return user[0]


def set_user_last_change(user_id, now):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("UPDATE users SET last_change = ? WHERE account_id = ?", [str(now), user_id])
    conn.commit()


def get_user_info(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE account_id = ?", [user_id])
    user = c.fetchone()
    return user


def get_user_vk(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT vk FROM users WHERE account_id = ?", [user_id])
    user = c.fetchone()
    print(user)
    return user[0]


def get_user_neighbours(user_id, room=None):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    user = get_user_info(user_id)
    print(user[2:4])
    if room:
        c.execute("SELECT * FROM users WHERE hostel = ? AND apartments = ? AND room = ? ", user[2:5])
    else:
        c.execute("SELECT * FROM users WHERE hostel = ? AND apartments = ?", user[2:4])
    possible_users = c.fetchall()
    print(possible_users)
    for i in possible_users:
        i = tuple(i)
    possible_users.remove(user)
    print(possible_users)
    return possible_users


def main():
    @bot.message_handler(commands=['/where'])


    @bot.message_handler(commands=['set_time_user'])
    def set_time(message):
        if white_list(message):
            print(message)
            cur = message.text.split()
            print(cur)
            if len(cur) == 1:
                cur.append(NONE_user)
            user_id = cur[1]
            if user_id != NONE_user:
                change_user_info('last_change', NONE_time, user_id)
            for admins_chat in admins_chat_id:
                print(message)
                text = ''.join(cur[2:])
                admin_log_message(admins_chat, 'Админ изменил время юзеру по id %s' % (
                    int(user_id)))

    @bot.message_handler(commands=['from'])
    def registration(message):
        first_check(message)
        past_time = datetime.datetime.now() - datetime.datetime.strptime(get_user_last_change(message.from_user.id),
                                                                         '%Y-%m-%d %H:%M:%S.%f')
        if past_time.days < 7:
            send_message(message.from_user.id,
                         'Извините, вы меняли место проживания меньше недели назад. До конца запрета осталось %s, но вы можете обратиться к администратору в вк.' % str(
                             datetime.timedelta(7) - past_time))
        else:
            data = message.text
            send_message(message.from_user.id,
                         'На какой улице и в каком доме вы живете? Для ответа используй кнопки снизу',
                         reply_markup=hostels_markup)
            commit_previous_command(message.from_user.id, 'from hostel')
        user_update(message)

    @bot.message_handler(commands=['send_user'])
    def send_user(message):
        if white_list(message):
            print(message)
            cur = message.text.split()
            print(cur)
            if len(cur) == 1:
                cur.append(NONE_user)
            if len(cur) == 2:
                cur.append(NONE_message)
            user_id = cur[1]
            send_message(user_id, ' '.join(cur[2:]))
            for admins_chat in admins_chat_id:
                print(message)
                text = ' '.join(cur[2:])
                admin_log_message(admins_chat, 'Админ написал юзеру по id %s: \n%s' % (
                    int(user_id), text))

    @bot.message_handler(commands=['sendall'])
    def send_all(message):
        if white_list(message):
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            all_users = c.fetchall()
            for user in all_users:
                send_message(user[1], message.text.replace('/sendall', '').strip())
            for admins_chat in admins_chat_id:
                admin_send_message(admins_chat, 'Админ написал всем: \n%s' % message.text)

    @bot.message_handler(commands=['userscount'])
    def print_users_count(message):
        if white_list(message):
            first_check(message)
            conn = sqlite3.connect('users.db')
            c = conn.cursor()
            c.execute("SELECT * FROM users")
            all_users = c.fetchall()
            send_message(message.from_user.id, str(len(all_users)))

    @bot.message_handler(commands=['help', 'start'])
    def help_message(message):
        if True:
            first_check(message)
            send_message(message.chat.id,
                         '/from для регистрации места проживания \n'
                         '/know для вывода своих соседей \n'
                         '/vk для регистрации вашего vk, т.к. у некоторых людей нет хендла в телеграме, и наш бот не может вас связать. ',
                         reply_markup=default_markup
                         )
            user_update(message)

    @bot.message_handler(commands=['stop'])
    def stop(message):
        first_check(message)
        user_id = message.from_user.id
        commit_previous_command(user_id, NONE_command)
        user_update(message)


    @bot.message_handler(commands=[])


    @bot.message_handler(commands=['know'])
    def know_your_neighbours(message):
        first_check(message)
        user_id = message.from_user.id
        send_message(user_id, "Ты хочешь найти соседей по...", reply_markup=know_markup)
        change_user_info('previous_command', 'know NONE', user_id)

    @bot.message_handler(commands=['vk'])
    def update_vk_url(message):
        first_check(message)
        send_message(message.from_user.id, "Вставьте ссылку на свой вк")
        change_user_info('previous_command', 'vk NONE', message.from_user.id)

    @bot.message_handler(content_types=['text'])
    def return_user_info(message):
        first_check(message)
        user_id = message.from_user.id
        chat_id = message.chat.id
        if chat_id in admins_chat_id:
            pass
        elif True:
            previous_command, attribute = get_previous_command(user_id).split()
            if previous_command == 'know':
                user = get_user_info(user_id)
                if user[2] != NONE_place and user[3] != NONE_place:
                    if 'по комнате' in message.text.lower():
                        room = True
                    else:
                        room = None
                    expected_users = get_user_neighbours(user_id, room)
                    print('expects = ', expected_users)
                    print(room)
                    if len(expected_users):
                        send_message(user_id,
                                     "Вот список всех ваших соседей, хендлы и имена в телеграме приводятся на момент последнего посещения нашего бота: \n")
                        for neighbour in expected_users:
                            if user != neighbour:
                                name = neighbour[0].split()
                                if len(name) < 2:
                                    name.insert(0, 'NONE')
                                send_message(user_id, "Хендл: @%s, имя: %s, ссылка на вк: %s, <a href='tg://user?id=%s'>"
                                                      ">ссылка на телеграм</a>" % (
                                    name[0], ' '.join(name[1:]), get_user_vk(neighbour[1]), user_id))
                        send_message(user_id,
                                     'Мы нашли нескольких ваших соседей, но, быть может, есть и другие!\nЧтобы быстрее узнать всех людей, с которыми живете, кидайте ссылку на бота друзьям, делайте репосты из нашей группы в вк (смотрите описание бота)')
                    else:
                        if message.text in ['по комнате', 'по квартире']:
                            send_message(user_id,
                                         'Похоже, что ваши соседи %s еще не зарегистрировались😔\nЧтобы быстрее узнать, с кем живете, кидайте ссылку на бота друзьям, делайте репосты из нашей группы в вк (смотрите описание бота)' % message.text)
                    change_user_info('previous_command', NONE_command, user_id)
                else:
                    send_message(user_id, 'Вы еще не зарегистрировались')
            elif previous_command == 'from':
                if attribute == 'hostel':
                    if message.text in hostels_dict.keys():
                        change_user_info('hostel', message.text, user_id)
                        commit_previous_command(user_id, "from room")
                        send_message(user_id,
                                     'Отправьте номер комнаты в том же формате, в котором он написан у вас в направлении, например 123(4)\nЛучше всего - скопировать\nЕсли не копируете, но в номере есть буквы, используйте русские буквы для ввода',
                                     reply_markup=NONE_markup)
                    else:
                        send_message(user_id,
                                     'Такого общежития нет, попробуйте воспользоваться кнопками снизу или напишите /stop, чтобы остановить регистрацию',
                                     reply_markup=hostels_markup)
                        for admin_chat in admins_chat_id:
                            admin_send_message(admin_chat, message)

                elif attribute == 'room':
                    text = message.text[:400]
                    text = text.replace('(', ' ').replace(')', ' ').split()
                    if len(text) < 2:
                        text.append(NONE_place)
                    change_user_info('apartments', text[0], user_id)
                    change_user_info('room', ''.join(text[1:]), user_id)
                    hostel, apartments, room = get_user_place(user_id)
                    if room:
                        send_message(user_id,
                                     'Подтвердите корректность введенных данных \nВы живете в %s квартире в %s комнате на %s, так? \nПрочитайте ВНИМАТЕЛЬНО' % (
                                         apartments, room, hostel),
                                     reply_markup=yesno_markup)
                    else:
                        send_message(user_id,
                                     'Подтвердите корректность введенных данных \nВы живете в %s квартире на %s, так? \nПрочитайте ВНИМАТЕЛЬНО' % (
                                         apartments, hostel),
                                     reply_markup=yesno_markup)
                    commit_previous_command(user_id, 'from sanity_check')
                else:
                    if message.text.lower() == 'да':
                        commit_previous_command(user_id, NONE_command)
                        send_message(user_id,
                                     'Вы успешно зарегистрировались. Используйте /know, чтобы узнать своих соседей, а также мы будем уведомлять вас о всех новых соседях.',
                                     reply_markup=NONE_markup)
                        neighbours = get_user_neighbours(user_id)
                        for neighbour in neighbours:
                            send_message(neighbour[1],
                                         "У вас появился новый сосед: %s, за более подробной информацией в /know" %
                                         get_user_info(user_id)[0])
                        set_user_last_change(user_id, datetime.datetime.now())

                    elif message.text.lower == 'нет':
                        commit_previous_command(user_id, NONE_command)
                        change_user_info('room', NONE_place, user_id)
                        change_user_info('hostel', NONE_place, user_id)
                        send_message(user_id,
                                     'Попробуйте еще раз зарегистрироваться, в следующий раз точно получится',
                                     reply_markup=NONE_markup)
                    else:
                        commit_previous_command(user_id, NONE_command)
                        change_user_info('room', NONE_place, user_id)
                        change_user_info('hostel', NONE_place, user_id)
                        send_message(user_id,
                                     'Попробуйте еще раз зарегистрироваться, в следующий раз точно получится',
                                     reply_markup=NONE_markup)
                        for admin_chat in admins_chat_id:
                            admin_send_message(admin_chat, message)

            elif previous_command == 'vk':
                vk = message.text[:400]
                change_user_info('vk', vk, user_id)
                send_message(user_id, "Ваша текущая ссылка на вк, которая будет показываться соседям: %s " % vk)
            else:
                send_message(user_id, "Мы пока разрабатываем разговорного бота, не торопитесь.",
                             reply_markup=NONE_markup)
                for admin_chat in admins_chat_id:
                    admin_send_message(admin_chat, message)
            user_update(message)

    bot.polling(timeout=150)


main()

while True:
    try:
        current_time = datetime.datetime.now()
        main()
    except Exception as e:
        if (datetime.datetime.now() - current_time).seconds > 5:
            f = open('log.txt', 'a')
            print(e, datetime.datetime.now(), file=f)
            f.close()
