# Generated by Django 4.2.2 on 2024-06-18 13:56

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("mailapp", "0024_alter_mailing_options_alter_mailinglog_log_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="mailing",
            name="message_in",
            field=models.TextField(
                blank=True,
                help_text="введите описание рассылки",
                null=True,
                verbose_name="описание",
            ),
        ),
        migrations.AlterField(
            model_name="mailing",
            name="user",
            field=models.ForeignKey(
                blank=True,
                help_text="пользователь",
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
                verbose_name="пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="mailinglog",
            name="log_text",
            field=models.TextField(
                default=datetime.datetime(
                    2024, 6, 18, 13, 56, 32, 226421, tzinfo=datetime.timezone.utc
                ),
                help_text="введите текст лога",
                verbose_name="текст лога",
            ),
        ),
    ]
