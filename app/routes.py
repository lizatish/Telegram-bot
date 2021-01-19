import requests
from flask import request, session

from app import app, bot
from app.models import User


@bot.message_handler(commands=['start'])
def start(message):

    if not User.query.get(message.from_user.chat.id).first():
        bot.reply_to(message, 'Вы новенький!')

    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@app.route('/' + app.config['TELEGRAM_TOKEN'], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://lizatish-telegram-bot.herokuapp.com/' + app.config['TELEGRAM_TOKEN'])
    return "!", 200


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


def get_weather():
    params = {"access_key": "36e33d4bb328e66fc587336724a295b4", "query": "Рязань"}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    if api_response['success']:
        return f"Сейчас в Рязани {api_response['current']['temperature']} градусов"
    else:
        return "Такой город не найден"
