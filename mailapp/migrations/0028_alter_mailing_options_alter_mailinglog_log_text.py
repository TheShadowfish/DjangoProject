# Generated by Django 4.2.2 on 2024-06-18 18:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mailapp", "0027_alter_mailinglog_log_text"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="mailing",
            options={
                "permissions": [
                    (
                        "can_turn_off_mailing",
                        "Can turn off mailing (mailing.settings.status = False",
                    )
                ],
                "verbose_name": "рассылка",
                "verbose_name_plural": "рассылки",
            },
        ),
        migrations.AlterField(
            model_name="mailinglog",
            name="log_text",
            field=models.TextField(
                default=datetime.datetime(
                    2024, 6, 18, 18, 33, 11, 491608, tzinfo=datetime.timezone.utc
                ),
                help_text="введите текст лога",
                verbose_name="текст лога",
            ),
        ),
    ]