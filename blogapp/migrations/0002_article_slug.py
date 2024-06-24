# Generated by Django 4.2.2 on 2024-06-24 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("blogapp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="article",
            name="slug",
            field=models.SlugField(
                help_text="slug", null=True, unique=True, verbose_name="slug"
            ),
        ),
    ]
