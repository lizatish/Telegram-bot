import requests
import telebot
from flask import request, session

from app import app, bot, db
from app.models import User


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@app.route('/' + app.config['TELEGRAM_TOKEN'], methods=['POST'])
def getMessage():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/")
def webhook():
    bot.remove_webhook()
    # bot.set_webhook(url='https://lizatish-telegram-bot.herokuapp.com/' + app.config['TELEGRAM_TOKEN'])
    bot.set_webhook(url='https://7308fa93b393.ngrok.io/' + app.config['TELEGRAM_TOKEN'])

    return "!", 200


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    user = User.query.filter_by(id=message.chat.id).first()
    if user is None:
        user = User(id=message.chat.id, first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name)

        db.session.add(user)
        db.session.commit()
        bot.reply_to(message, 'Вы зарегистрированы!')
    else:
        bot.reply_to(message, f'Всего пользователей {User.query.count()}')
        for user in User.query.all():
            bot.reply_to(message, f'{user.first_name} {user.last_name}')


def get_weather():
    params = {"access_key": "36e33d4bb328e66fc587336724a295b4", "query": "Рязань"}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    if api_response['success']:
        return f"Сейчас в Рязани {api_response['current']['temperature']} градусов"
    else:
        return "Такой город не найден"
