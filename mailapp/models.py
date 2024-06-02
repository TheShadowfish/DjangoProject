from django.db import models

# Create your models here.

class Mail(models.Model):
    email = models.EmailField(max_length=150, verbose_name='почта')


    def __str__(self):
        return f"{self.boat} от {self.email}"

    class Meta:
        verbose_name = ''
        verbose_name_plural = 'заказы'