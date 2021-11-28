from django.test import TestCase
from src.bot import views
from src.bot import pizzordbot
import os
import telebot


# Create your tests here.

class TestTelegramBot(TestCase):
    def setUp(self) -> None:
        self.bot = pizzordbot.PizzordBot("TEST")
        views.bot = self.bot
        telebot.apihelper.CUSTOM_REQUEST_SENDER = self.custom_sender

    def custom_sender(method, url, message, **kwargs):
        result = telebot.util.CustomRequestResponse(
            '{"ok":true,"result":{"message_id": 1, "date": 1, "chat": {"id": 1, "type": "private"}}}')
        return result

    def test_pizza_correct_choice_big(self):
        self.bot.started()
        answer = views.send_message("test", chat_id=1, text='большую')
        self.assertEqual(answer, 'Как вы будете платить?')

    def test_pizza_correct_choice_small(self):
        self.bot.started()
        answer = views.send_message("test", chat_id=1, text='маленькую')
        self.assertEqual(answer, 'Как вы будете платить?')

    def test_chose_pizza_incorrect_answer(self):
        self.bot.started()
        answer = views.send_message("test", chat_id=1, text='среднюю')
        self.assertEqual(answer, 'Такой у нас нет. Выберите большую или маленькую')

    def test_chose_payment_correct_answer_cash(self):
        self.bot.started()
        self.bot.pizza_chosed()
        answer = views.send_message("test", chat_id=1, text='наличными')
        self.assertEqual(answer, 'Вы выбрали default пиццу. Оплата - наличными?')

    def test_chose_payment_correct_answer_card(self):
        self.bot.started()
        self.bot.pizza_chosed()
        answer = views.send_message("test", chat_id=1, text='картой')
        self.assertEqual(answer, 'Вы выбрали default пиццу. Оплата - картой?')

    def test_chose_payment_incorrect_answer(self):
        self.bot.started()
        self.bot.pizza_chosed()
        answer = views.send_message("test", chat_id=1, text='тугриками')
        self.assertEqual(answer, 'Некорректный способ оплаты. Выберите - картой или наличными')

    def test_correct_confirmation_answer_yes(self):
        self.bot.started()
        self.bot.pizza_chosed()
        self.bot.payment_chosed()
        answer = views.send_message("test", chat_id=1, text='да')
        self.assertEqual(answer, 'Ваш заказ подтвержден!')

    def test_correct_confirmation_answer_no(self):
        self.bot.started()
        self.bot.pizza_chosed()
        self.bot.payment_chosed()
        answer = views.send_message("test", chat_id=1, text='нет')
        self.assertEqual(answer, 'Чтобы начать сначала введите "/start"')

    def test_incorrect_confirmation_answer(self):
        self.bot.started()
        self.bot.pizza_chosed()
        self.bot.payment_chosed()
        answer = views.send_message("test", chat_id=1, text='не помню')
        self.assertEqual(answer, 'Для подтверждения заказа введите "Да", для отмены "Нет"')
