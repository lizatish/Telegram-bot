import os

import requests
import telebot
from flask import request

from app import app

bot = telebot.TeleBot(token='1439238476:AAFuJ4R1nkDyLDPMpDNPwK2HLQhrPTQ65d4')


# @app.route("/", methods=["GET", "POST"])
# def hello_world():
#     if request.method == "POST":
#         chat_id = request.json["message"]["chat"]["id"]
#         send_message(chat_id, f'Hello,  {request.json["message"]["from"]["first_name"]}!')
#         send_message(chat_id, get_weather())
#     return 'Hello, World!'


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(
        url="https://lizatish-telegram-bot.herokuapp.com/")  # этот url нужно заменить на url вашего Хероку приложения
    return "?", 200


def send_message(chat_id, text):
    method = "sendMessage"
    token = "1439238476:AAFuJ4R1nkDyLDPMpDNPwK2HLQhrPTQ65d4"
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = {"chat_id": chat_id, "text": text}
    requests.post(url, data=data)


@app.route("/bot", methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


def get_weather():
    params = {"access_key": "36e33d4bb328e66fc587336724a295b4", "query": "Рязань"}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    if api_response['success']:
        return f"Сейчас в Рязани {api_response['current']['temperature']} градусов"
    else:
        return "Такой город не найден"
