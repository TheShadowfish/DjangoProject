from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailapp.forms import UserForm
from mailapp.models import Mail, User, Mailing


# from django.apps.config import models.Mail

class MailListView(ListView):
    model = Mail


class UserListView(ListView):
    model = User


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailapp:user_list')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    success_url = reverse_lazy('mailapp:user_list')


class UserDetailView(DetailView):
    model = User


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('mailapp:user_list')


class MailingListView(ListView):
    model = Mailing



