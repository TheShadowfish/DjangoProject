from django.forms import inlineformset_factory
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailapp.forms import UserForm, MailingForm, MailForm
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


class MailFormsetMixin():
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mail_form_set = inlineformset_factory(Mailing, Mail, form=MailForm, extra=1)
        context['formset'] = mail_form_set()
        if self.request.method == 'POST':
            context['formset'] = mail_form_set(self.request.POST, instance=self.object)
        else:
            context['formset'] = mail_form_set(instance=self.object)
        return context

    def form_valid(self, form):
        formset = self.get_context_data()['formset']
        self.object = form.save()

        if formset.is_valid():
            formset.instance = self.object
            formset.save()

        return super().form_valid(form)


class MailingCreateView(MailFormsetMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')


class MailingUpdateView(MailFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')
