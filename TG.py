# -*- coding: utf-8 -*-
# version: 1.1

import time
import file_with_data
import random
import smtplib
import telebot
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from telebot import types

bot = telebot.TeleBot(file_with_data.token)
downloaded_file = False


def loger(time_error, text_error):
    log = open("log.txt", "a")
    str(text_error)
    log.write("\n")
    log.write(time_error)
    log.write("\n")
    log.write(text_error)
    log.close()


def times() -> str:
    tym = time.localtime()
    opt = str(time.strftime("%d/%m/%Y %H:%M:%S", tym))
    return opt


def nuber_req() -> str:
    tym = time.localtime()
    opt = str(time.strftime("%d%m%Y%H%M%S", tym))
    return opt + str(random.randint(0, 1000))


def img_name() -> str:
    tym = time.localtime()
    opt = str(time.strftime("%d_%m_%Y", tym))
    number = str(random.randint(0, 1000))
    name = number + "img" + opt + ".jpg"
    return name


def mailsend(message, flag):
    MailServer = smtplib.SMTP(f'{file_with_data.mail_host}', 25)
    MailServer.ehlo()
    MailServer.starttls()
    MailServer.ehlo()
    MailServer.login(file_with_data.mail_login, file_with_data.mail_pass)
    msg = MIMEMultipart()
    msg["Subject"] = f"{theme}"
    msg["From"] = file_with_data.mail_login
    msg["To"] = file_with_data.mail_to
    mes = f"{problem}  \n\n Номер заявки: #{times()}{random.randint(0, 1000)} \n\n ФИО: {l_name} " \
          f"\n\n НИК:{str(message.chat.first_name)} " \
          f"\n\n Тел: {number_user} \n\n Представительство: {loc}"
    msg.attach(MIMEText(mes))
    if downloaded_file and flag:
        msg.attach(MIMEImage(downloaded_file))
    MailServer.send_message(msg)
    MailServer.quit()


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id, f"Здраствуйте, {user_first_name}".format(message.from_user.id))
    reg_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    markup.add(reg_button)
    bot.send_message(message.chat.id, 'Оставьте ваш контактный номер чтобы тех.поддержка могла связаться с вами',
                     reply_markup=markup)
    bot.register_next_step_handler(message, name)


@bot.message_handler(commands=['help'])
def help_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Создать заявку")
    markup.add(btn1)
    user_first_name = str(message.chat.first_name)
    bot.send_message(message.chat.id, f"Здраствуйте, {user_first_name}, это бот для создания заявок. Чтобы создать "
                                      f"заявку нажмите 'Создать заявку' и следуйте инструкциям. "
                                      f"Если возникли трудности с ботом напишите сюда:  ".format(message.from_user.id),
                     reply_markup=markup)


@bot.message_handler(content_types=['text', 'photo'])

def name(message):
    global number_user
    number_user = message.contact.phone_number
    bot.send_message(message.chat.id, "Отправьте ваше ФИО")
    bot.register_next_step_handler(message, location)


def location(message):
    global l_name
    l_name = message.text
    bot.send_message(message.chat.id, "Отправьте наименование вашего представительства")
    bot.register_next_step_handler(message, first_step)


def first_step(message):
    try:
        global loc
        loc = message.text
        user_first_name = str(message.chat.first_name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        btn1 = types.KeyboardButton("Назад")
        markup.add(btn1)
        markup = types.ReplyKeyboardRemove()
        bot.send_message(message.chat.id, f"{user_first_name}, напишите тему заявки".format(message.from_user.id),
                         reply_markup=markup)
        bot.register_next_step_handler(message, theme_def)
    except:
        if message.text != "/start" and message.text != "/help":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            reg_button = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
            markup.add(reg_button)
            bot.send_message(message.chat.id,
                             'Оставьте ваш контактный номер чтобы тех.поддержка могла связаться с вами',
                             reply_markup=markup)
            bot.register_next_step_handler(message, first_step)
    match message.text:
        case "/start":
            start_message(message)
        case "/help":
            help_message(message)
        case "Назад":
            start_message(message)


def theme_def(message):
    user_first_name = str(message.chat.first_name)
    global theme
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton("Назад")
    markup.add(btn1)
    match message.text:
        case "/start":
            start_message(message)
        case "/help":
            help_message(message)
        case "Назад":
            start_message(message)
        case _:
            theme = message.text
            bot.send_message(message.chat.id, f"{user_first_name}, опишите вашу проблему".format(message.from_user.id),
                             reply_markup=markup)
            bot.register_next_step_handler(message, problem_def)


def problem_def(message):
    user_first_name = str(message.chat.first_name)
    global problem
    problem = message.text
    match message.text:
        case "Назад":
            bot.send_message(message.chat.id, f"{user_first_name}, напишите тему заявки".format(message.from_user.id))
            bot.register_next_step_handler(message, theme_def)
        case "/start":
            start_message(message)
        case "/help":
            help_message(message)
        case _:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn1 = types.KeyboardButton("Пропустить")
            btn2 = types.KeyboardButton("Назад")

            markup.row(btn1, btn2)
            bot.send_message(message.chat.id,
                             "Вы можете добавить изображение к вашей заявке ".format(message.from_user.id),
                             reply_markup=markup)
            bot.register_next_step_handler(message, next_step)


def next_step(message):
    user_first_name = str(message.chat.first_name)
    match message.text:
        case "Пропустить":
            end(message, False)
        case "/start":
            start_message(message)
        case "/help":
            help_message(message)
        case "Назад":
            bot.send_message(message.chat.id, f"{user_first_name}, опишите вашу проблему".format(message.from_user.id))
            bot.register_next_step_handler(message, problem_def)
        case _:
            @bot.message_handler(content_types=['photo'])
            def photo(message):
                global downloaded_file
                fileID = message.photo[-1].file_id
                file_info = bot.get_file(fileID)
                downloaded_file = bot.download_file(file_info.file_path)
                name_photo = img_name()
                with open(f"{name_photo}", 'wb') as new_file:
                    new_file.write(downloaded_file)

            try:
                photo(message)
                end(message, True)
            except:
                end(message, False)


def end(message, flag):
    global key
    key = times() + str(random.randint(0, 1000))
    fs = open("req_list.txt", "a")
    fs.write("\n")
    fs.write(
        f'Тема заявки: {theme} Текст заявки: {problem} Номер заявки: #{key} ФИО:{l_name} НИК:{str(message.chat.first_name)} Тел: {number_user} Представительство: {loc}')
    fs.close()

    try:
        bot.send_message(file_with_data.id_support,
                         f"Тема заявки: {theme} \n Текст заявки: {problem} \n ФИО:{l_name} \n НИК:{str(message.chat.first_name)}\n Номер телефона: {number_user} \n Представительство: {loc}")
        if downloaded_file and flag:
            bot.send_photo(file_with_data.id_support, downloaded_file)
            mailsend(message, True)
        else:
            mailsend(message, False)
        bot.send_message(message.chat.id,
                         "Заявка принята ✅ \n Для создания новой заявки нажмите > /start".format(
                             message.from_user.id),
                         reply_markup=types.ReplyKeyboardRemove())
    except Exception as err:
        bot.send_message(message.chat.id,
                         "Произошла ошибка ❌ \n Для создания новой заявки нажмите > /start".format(
                             message.from_user.id),
                         reply_markup=types.ReplyKeyboardRemove())
        time_error = "Mail error " + times()
        text_error = "Error: \"{}\"".format(err)
        print(time_error, "\n", text_error)
        loger(time_error, text_error)
    bot.register_next_step_handler(message, start_message)


def main():
    try:
        bot.infinity_polling()
    except Exception as err:
        time_error = "Bot error" + times()
        text_error = "Error: \"{}\"".format(err)
        loger(time_error, text_error)
        print(time_error, "\n", text_error)
        main()


if __name__ == '__main__':
    main()
