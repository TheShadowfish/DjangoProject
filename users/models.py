from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    username = None

    email = models.EmailField(max_length=150, verbose_name='почта', unique=True, help_text='Введите вашу почту')
    name = models.CharField(max_length=150, verbose_name='имя пользователя', help_text='Введите ваше имя')
    description = models.TextField(verbose_name='описание', help_text='Введите дополнительную информацию', **NULLABLE)
    phone_number = PhoneNumberField(**NULLABLE, verbose_name='телефон', help_text='Введите ваш номер телефона')
    avatar = models.ImageField(upload_to='users/avatars/', verbose_name='аватар', help_text='Выберите аватар', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='активен', )
    is_admin = models.BooleanField(default=False, verbose_name='админ', )
    is_moderator = models.BooleanField(default=False, verbose_name='модератор', )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        return f" {self.name} ({self.email})"
