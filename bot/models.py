from django.db import models


# Create your models here.

class BotState(models.Model):
    chat_id = models.IntegerField(primary_key=True)
    state = models.CharField(max_length=50, default='start')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, null=True, blank=True)


class Order(models.Model):
    pizza_size = models.CharField(max_length=50, null=True, blank=True)
    payment = models.CharField(max_length=50, null=True, blank=True)
