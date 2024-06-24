# Generated by Django 4.2.2 on 2024-06-19 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        help_text="Введите заголовок статьи",
                        max_length=100,
                        verbose_name="Заголовок",
                    ),
                ),
                (
                    "body",
                    models.TextField(
                        help_text="Введите содержимое статьи",
                        verbose_name="Содержимое статьи",
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="Загрузите превью статьи",
                        null=True,
                        upload_to="blog/photo",
                        verbose_name="Превью",
                    ),
                ),
                (
                    "created_at",
                    models.DateField(
                        auto_now_add=True,
                        help_text="Укажите дату создания",
                        null=True,
                        verbose_name="Дата создания",
                    ),
                ),
                (
                    "is_published",
                    models.BooleanField(
                        default=True,
                        help_text="Укажите признак публикации",
                        verbose_name="Признак публикации",
                    ),
                ),
                (
                    "views_count",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="Укажите количество просмотров",
                        verbose_name="Количество просмотров",
                    ),
                ),
            ],
            options={
                "verbose_name": "Запись в блоге",
                "verbose_name_plural": "Записи в блоге",
            },
        ),
    ]
