from .models import BotState, Order


def save_state(chat_id: int, state: str) -> None:
    try:
        BotState.objects.filter(chat_id=chat_id).update(state=state)
    except BotState.DoesNotExist:
        BotState.objects.create(chat_id=chat_id, state=state)


def get_state(chat_id: int) -> str:
    state = BotState.objects.get(chat_id=chat_id).state
    return state


def save_order(chat_id: int, pizza_size: str, payment: str) -> None:
    order = Order(pizza_size=pizza_size, payment=payment)
    order.save()
    BotState.objects.filter(chat_id=chat_id).update(order=order)
