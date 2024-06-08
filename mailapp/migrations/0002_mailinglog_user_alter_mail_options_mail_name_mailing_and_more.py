# Generated by Django 5.0.6 on 2024-06-08 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('log_text', models.TextField(help_text='введите текст лога', verbose_name='текст лога')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='введите дату создания лога', verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата')),
            ],
            options={
                'verbose_name': 'лог рассылки',
                'verbose_name_plural': 'логи рассылок',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='имя пользователя')),
                ('email', models.EmailField(max_length=150, verbose_name='почта')),
            ],
        ),
        migrations.AlterModelOptions(
            name='mail',
            options={'verbose_name': 'емайл', 'verbose_name_plural': 'емайлы'},
        ),
        migrations.AddField(
            model_name='mail',
            name='name',
            field=models.CharField(default='Уважаемый клиент!', max_length=150, verbose_name='имя получателя'),
        ),
        migrations.CreateModel(
            name='Mailing',
            fields=[
                ('title', models.CharField(help_text='введите название рассылки', max_length=150, unique=True, verbose_name='рассылка')),
                ('message', models.TextField(help_text='введите текст рассылки', verbose_name='сообщение')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='введите дату создания рассылки', verbose_name='дата создания')),
                ('status', models.BooleanField(default=False, help_text='введите статус рассылки', verbose_name='статус')),
                ('datetime_send', models.DateTimeField(help_text='введите дату срабатывания', verbose_name='дата срабатывания')),
                ('mailing_log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='mailing_log', serialize=False, to='mailapp.mailinglog', verbose_name='лог рассылки')),
                ('user', models.ForeignKey(help_text='пользователь', on_delete=django.db.models.deletion.CASCADE, related_name='user', to='mailapp.user', verbose_name='пользователь')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.AddField(
            model_name='mail',
            name='mailing',
            field=models.ForeignKey(blank=True, help_text='рассылка', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mailing', to='mailapp.mailing', verbose_name='рассылка'),
        ),
    ]