from django.contrib import admin
from django.urls import path
from . import views
import os

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

urlpatterns = [
    path('webhook', views.webhook, name='webhook'),
    path(f'{TOKEN}', views.get_message, name="get_message"),
    path('admin/', admin.site.urls),
]