import telebot
import os
import traceback
import pandas as pd
import random
import difflib
import subprocess

# Замените 'YOUR_TOKEN' на ваш токен бота
TOKEN = '7117986911:AAGLCRk1sjZCs_FuaVNET5PZTdmJb_G60lo'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Пришли мне свой код для проверки.")


@bot.message_handler(func=lambda message: True)
def check_code(message):
    # Получаем сообщение с кодом от пользователя
    user_code = message.text

    # Создаем временный файл для кода с явным указанием кодировки UTF-8
    file_path = 'temp_code.py'
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(user_code)

    # Проверяем синтаксис кода
    try:
        subprocess.check_output(['python', '-m', 'py_compile', file_path], stderr=subprocess.STDOUT)

        # Проверяем код на основе заданных тестов
        exec(compile(user_code, file_path, 'exec'))
        bot.reply_to(message, "Код написан верно!")
    except subprocess.CalledProcessError as e:
        bot.reply_to(message, f"Ошибка синтаксиса: {e.output.decode()}")
    except Exception as e:
        bot.reply_to(message, f"Ошибка выполнения кода: {e}")
    finally:
        os.remove(file_path)  # Удаляем временный файл


bot.polling()