# Generated by Django 4.2.2 on 2024-06-16 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="name",
            field=models.CharField(
                blank=True,
                help_text="Введите ваше имя",
                max_length=150,
                null=True,
                verbose_name="имя пользователя",
            ),
        ),
    ]
