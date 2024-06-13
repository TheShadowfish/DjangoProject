# Generated by Django 5.0.6 on 2024-06-13 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailapp", "0013_alter_mailinglog_log_text_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="datetime_send",
            field=models.DateTimeField(
                auto_now_add=True,
                help_text="введите дату срабатывания",
                verbose_name="дата срабатывания",
            ),
        ),
        migrations.AlterField(
            model_name="mailinglog",
            name="log_text",
            field=models.TextField(
                default=datetime.datetime(
                    2024, 6, 13, 14, 26, 26, 912543, tzinfo=datetime.timezone.utc
                ),
                help_text="введите текст лога",
                verbose_name="текст лога",
            ),
        ),
        migrations.AlterField(
            model_name="mailingsettings",
            name="datetime_send",
            field=models.DateTimeField(
                help_text="введите дату и время первой отправки рассылки",
                verbose_name="дата и время первой отправки рассылки",
            ),
        ),
    ]