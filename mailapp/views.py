from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from mailapp.forms import UserForm
from mailapp.models import Mail, User


# from django.apps.config import models.Mail

class MailListView(ListView):
    model = Mail
    fields = ('email')


class UserListView(ListView):
    model = User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailapp:user_list')


class UserDetailView(DetailView):
    model = User
