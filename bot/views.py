import os
from django.http.response import HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from .pizzordbot import PizzordBot
from .models import Order, BotState
from .db import save_state, save_order, get_state

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')
bot = PizzordBot(TOKEN)
order = {1: {'size': 'default', 'payment': 'default'}}


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
def start_message(message: telebot.types.Message) -> str:
    """Обработчик команды /start"""
    bot.started()  # переход в следующее состояние - chosing_pizza
    chat_id = message.chat.id
    state = bot.state  # state = chosing_pizza
    save_state(chat_id, state)
    answer = f'Какую вы хотите пиццу? Большую или маленькую?'
    bot.send_message(chat_id, answer)
    order[chat_id] = {}
    return answer


@bot.message_handler(content_types=['text'])
def send_message(message: telebot.types.Message, chat_id=None, text=None) -> str:
    """Обработчик всех текстовых сообщений"""
    if not chat_id:
        chat_id = message.chat.id
    if not text:
        text = message.text.lower().strip()
    state = get_state(chat_id)  # получение текущего состояния бота

    if state == 'chosing_pizza':
        if text == 'большую' or text == 'маленькую':  # проверка корректности размера пиццы
            order[chat_id]['size'] = text  # сохранение значения в словаре
            bot.pizza_chosed()  # переход в следующее состояние "payment_chosing"
            save_state(chat_id, bot.state)  # сохранение состояния в базе данных
            answer = 'Как вы будете платить?'
            bot.send_message(chat_id, answer)  # отправка ответа в чат
        else:
            answer = f'Такой у нас нет. Выберите большую или маленькую'
            bot.send_message(chat_id, answer)
    elif state == 'chosing_payment':
        if text == 'наличными' or text == 'картой':  # проверка корректности способа оплаты
            order[chat_id]['payment'] = text  # сохранение значния в словаре
            bot.payment_chosed()  # переход в следующее состояние "confirmation"
            save_state(chat_id, bot.state)  # сохранение состояния в базе данных
            answer = f"Вы выбрали {order[chat_id]['size']} пиццу. Оплата - {order[chat_id]['payment']}?"
            bot.send_message(chat_id, answer)  # отправка ответа в чат
        else:
            answer = f'Некорректный способ оплаты. Выберите - картой или наличными'
            bot.send_message(chat_id, answer)
    elif state == 'confirmation':
        if text == 'да':  # заказ подтвержден пользователем
            bot.confirmed()  # переход в конечное состояние "finish"
            save_state(chat_id, bot.state)  # сохранение состояния в базе данных
            answer = f"Ваш заказ подтвержден!"
            bot.send_message(chat_id, answer)  # отправка ответа
            save_order(chat_id, order[chat_id]['size'], order[chat_id]['payment'])  # сохранение заказа в базе данных
        elif text == 'нет':
            bot.not_confirmed()  # при неподтверждении заказа - переход в начальное состояние "start"
            save_state(chat_id, bot.state)  # сохранение состояния
            answer = f'Чтобы начать сначала введите "/start"'
            bot.send_message(chat_id, answer)  # отправка ответа
        else:
            answer = f'Для подтверждения заказа введите "Да", для отмены "Нет"'
            bot.send_message(chat_id, answer)
    else:
        answer = f'Я не получил сообщение. Повторите, пожалуйста.\nЧтобы начать сначала введите "/start"'
        bot.send_message(chat_id, answer)
    return answer
