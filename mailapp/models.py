from django.db import models

NULLALE = {'blank': True, 'none': True}
# Create your models here.

class Mail(models.Model):
    email = models.EmailField(max_length=150, verbose_name='почта')


    def __str__(self):
        return f" {self.email}"

    class Meta:
        verbose_name = 'емайл'
        verbose_name_plural = 'емайлы'