import os
from django.http.response import HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from .pizzordbot import PizzordBot

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
bot = PizzordBot(TOKEN)
order = {1: {'size': 'default', 'payment': 'default'}}
sizes = ['большая', 'большую', 'маленькая', 'маленькую']
payments = ['карта', 'картой', 'наличные', 'наличными']


def webhook(request):
    """Установка webhook к API Telegram"""
    bot.remove_webhook()
    bot.set_webhook(url='https://pizzordbot.herokuapp.com/' + TOKEN)
    return HttpResponse(status=200)


@csrf_exempt
def get_message(request):
    """Получение update от API Telegram"""
    json_string = request.body.decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def start_message(message):
    """Обработчик команды /start"""
    chat_id = message.chat.id
    bot.started()
    bot.send_message(chat_id, 'Какую вы хотите пиццу? Большую или маленькую?')
    order[chat_id] = {}


@bot.message_handler(content_types=['text'])
def send_message(message, chat_id=None, text=None):
    """Обработчик всех текстовых сообщений"""
    if not chat_id:
        chat_id = message.chat.id
    if not text:
        text = message.text
    state = bot.state
    if state == 'chosing_pizza':
        if text.lower() in sizes:
            order[chat_id]['size'] = text.lower()
            bot.pizza_chosed()
            answer = 'Как вы будете платить?'
            bot.send_message(chat_id, answer)
        else:
            answer = 'Такой у нас нет. Выберите большую или маленькую'
            bot.send_message(chat_id, answer)
    elif state == 'chosing_payment':
        if text.lower() in payments:
            order[chat_id]['payment'] = text.lower()
            bot.payment_chosed()
            answer = f"Вы выбрали {order[chat_id]['size']} пиццу. Оплата - {order[chat_id]['payment']}?"
            bot.send_message(chat_id, answer)
        else:
            answer = 'Некорректный способ оплаты. Выберите - картой или наличными'
            bot.send_message(chat_id, answer)
    elif state == 'confirmation':
        if text.lower() == 'да':
            bot.confirmed()
            answer = "Ваш заказ подтвержден!"
            bot.send_message(chat_id, answer)
        elif text.lower() == 'нет':
            bot.not_confirmed()
            answer = 'Чтобы начать сначала введите "/start"'
            bot.send_message(chat_id, answer)
        else:
            answer = 'Для подтверждения заказа введите "Да", для отмены "Нет"'
            bot.send_message(chat_id, answer)
    else:
        answer = 'Какую вы хотите пиццу? Большую или маленькую?'
        bot.send_message(chat_id, answer)

    return answer
