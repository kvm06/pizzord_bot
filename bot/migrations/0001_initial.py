# Generated by Django 3.2.9 on 2021-11-28 16:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pizza_size', models.CharField(blank=True, max_length=50, null=True)),
                ('payment', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BotState',
            fields=[
                ('chat_id', models.IntegerField(primary_key=True, serialize=False)),
                ('state', models.CharField(default='start', max_length=50)),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bot.order')),
            ],
        ),
    ]
