from transitions import Machine
from telebot import TeleBot

states = ['start', 'chosing_pizza', 'chosing_payment', 'confirmation', 'finish']

class PizzordBot(TeleBot):
    def __init__(self, token):
        super().__init__(token)
        self.machine = Machine(model=self, states=states, initial='start')
        self.machine.add_transition(trigger='started', source='*', dest='chosing_pizza')
        self.machine.add_transition(trigger='pizza_chosed', source='chosing_pizza', dest='chosing_payment')
        self.machine.add_transition(trigger='payment_chosed', source='chosing_payment', dest='confirmation')
        self.machine.add_transition(trigger='confirmed', source='confirmation', dest='finish')
        self.machine.add_transition(trigger='not_confirmed', source='confirmation', dest='start')

