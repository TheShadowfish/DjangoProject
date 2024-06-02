from django.shortcuts import render
from django.views.generic import ListView
from .models import Mail

class MailListView(ListView):
    model = Mail
    fields = ('email')