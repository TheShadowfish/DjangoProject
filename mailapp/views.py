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


class MailingCreateView(CreateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')

    def get_context_data(self, **kwargs):
        context = super(MailingCreateView, self).get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mailing, Mail, MailForm, extra=1)
        if self.request.POST:
            context['formset'] = MailForm(self.request.POST, instance=self.object)
        else:
            context['formset'] = MailForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class MailingUpdateView(UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')

    def get_context_data(self, **kwargs):
        context = super(MailingUpdateView, self).get_context_data(**kwargs)
        MailingFormset = inlineformset_factory(Mailing, Mail, MailForm, extra=1)
        if self.request.POST:
            context['formset'] = MailForm(self.request.POST, instance=self.object)
        else:
            context['formset'] = MailForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()

            return super().form_valid(form)

        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
