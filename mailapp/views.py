import random

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView

from blogapp.models import Article
from mailapp.forms import MailingForm, ClientForm, MessageForm, MailingSettingsForm, \
    MailingSettingsModeratorForm
from mailapp.models import Client, Mailing, MailingLog, Message, MailingSettings
from mailapp.services import sending
from mailapp.utils.utils import get_info_and_send, select_mailings
from users.models import User

ONLY_USERS_PROPERTY = True


# from django.apps.config import models.Mail

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = "users:login"

    # redirect_field_name = "login"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['only_users'] = ONLY_USERS_PROPERTY
        return context


class GetFormKwargsGetUserMixin:
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class GetFormClassUserIsOwnerMixin:
    def get_form_class(self):
        user = self.request.user
        if user == self.object.mailing.user:
            return ClientForm
        raise PermissionDenied


class ClientCreateView(LoginRequiredMixin, GetFormKwargsGetUserMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientUpdateView(LoginRequiredMixin, GetFormKwargsGetUserMixin, GetFormClassUserIsOwnerMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientDeleteView(LoginRequiredMixin, GetFormKwargsGetUserMixin, GetFormClassUserIsOwnerMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailapp:mail_list')


class ClientDetailView(LoginRequiredMixin, GetFormClassUserIsOwnerMixin, DetailView):
    model = Client


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['only_send'] = False
        return context


class MailingListViewSend(LoginRequiredMixin, ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['only_send'] = True
        return context


class MailingCreateAndFormsetMixin:

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        mail_form_set = inlineformset_factory(Mailing, Client, form=ClientForm, extra=1)
        context['formset'] = mail_form_set()
        if self.request.method == 'POST':
            context['formset'] = mail_form_set(self.request.POST, instance=self.object)
        else:
            context['formset'] = mail_form_set(instance=self.object)
        return context

    def form_valid(self, form):

        # Xозяином рассылки автоматически становится тот, кто её создал
        mailing = form.save()
        user = self.request.user
        # Что же я его owner не назвал сразу... теперь поздняк метаться.
        mailing.user = user
        mailing.save()

        # Сохранение сообщения рассылки обязательно, так как связь 1 к 1 и рассылка без сообщения не имеет смысла
        if mailing.message is None:
            message = Message.objects.create(title=f"{mailing.title} - first ",
                                             body=f"{mailing.message_in} - first creation")
            message.save()
            mailing.message = message
            # print(f'Сохранение сообщения {mailing.message}')
            mailing.save()
            # print('mailing.save()')
        else:
            message = Message.objects.get(id=mailing.message_id)

        # Сохранение настроек рассылки обязательно, связь 1 к 1 и рассылка без настроек не имеет смысла
        if mailing.settings is None:
            settings = MailingSettings.objects.create()
            settings.save()
            mailing.settings = settings
            # print(f'Сохранение настроек {mailing.settings}')
            mailing.save()
            # print('settings.save()')

        # Лог рассылки - создание и изменение тоже туда пишутся, не только попытки отправки
        log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', status=False, mailing=mailing)
        log.save()
        # print('log.save()')

        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = mailing
            formset.save()

        redirect_url = reverse('mailapp:message_settings_update', args=[message.id])

        self.success_url = redirect_url

        return super().form_valid(form)


class MailingCreateView(LoginRequiredMixin, MailingCreateAndFormsetMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailapp:mailing_list')  # object.pk


class MailingUpdateView(LoginRequiredMixin, MailingCreateAndFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')

    def get_form_class(self):
        user = self.request.user
        if user == self.object.user:
            return MailingForm
        raise PermissionDenied


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailapp:mailing_list')

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user:
            return
        else:
            raise PermissionDenied


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = MailingLog.objects.filter(mailing=self.object)
        context['clients'] = Client.objects.filter(mailing=self.object)
        context['message'] = Message.objects.get(id=self.object.message_id)
        context['settings'] = MailingSettings.objects.get(id=self.object.settings_id)
        return context

    def form_valid(self, form):
        user = self.request.user
        if user == self.object.user or user.has_perm("mailapp.view_mailing"):
            return
        else:
            raise PermissionDenied


# class MessageCreateView(LoginRequiredMixin, CreateView):
#     model = Message
#     form_class = MessageForm
#     success_url = reverse_lazy('mailapp:message_list')

class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['message_id'] = self.object.id

        mailing_owner = get_object_or_404(Mailing, message_id=self.object.id)
        user = self.request.user
        print(f"user={user}, mailing_owner.user= {mailing_owner.user}")
        context['owner'] = mailing_owner.user

        if user != mailing_owner.user:
            raise PermissionDenied

        return context


class MessageSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:mailing_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Mailing.objects.get(message_id=self.object.id)

        return context

    #
    def form_valid(self, form):
        mailing = self.get_context_data()['mailing']

        redirect_url = reverse('mailapp:settings_update', args=[mailing.settings_id])

        self.success_url = redirect_url

        return super().form_valid(form)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context['only_users'] = ONLY_USERS_PROPERTY

        return context


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailapp:settings_list')

    # В других методах получить object.id не вышло
    # потому что: The view's object attribute is set during get/post by BaseUpdateView
    # So it is not yet available in the dispatch method. But it will be available in the get_success_url and get_context_data methods as those happen after get/post.
    # PS Django реально сложен...

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['settings_id'] = self.object.id

        mailing_owner = get_object_or_404(Mailing, settings_id=self.object.id)
        user = self.request.user
        print(f"user={user}, mailing_owner.user= {mailing_owner.user}")
        context['owner'] = mailing_owner.user

        if user != mailing_owner.user:
            raise PermissionDenied
        return context


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        context['only_users'] = ONLY_USERS_PROPERTY
        return context


@login_required
def mailing_send(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)

    print(f"mailing_send {mailing_item}")

    try:
        # sending(mailing_item)
        get_info_and_send(mailing_item)
    except Exception as e:
        print("FUCKING ERROR!!!")
        print(e)
    else:
        mailing_item.status = True
        mailing_item.save()

    print(mailing_item)
    # print(mailing_item.status)

    select_mailings()

    return redirect(reverse('mailapp:mailing_list'))


@login_required
@permission_required('mailapp.can_turn_off_mailing')
def toggle_activity_mailing(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)
    if mailing_item.settings.status:
        mailing_item.settings.status = False
    else:
        mailing_item.settings.status = True

    mailing_item.settings.save()

    return redirect(reverse('mailapp:mailing_list'))


# Та самая главная страница, которую мы должны реализовать
class HomePageView(TemplateView):
    template_name = "mailapp/home.html"

    def get_context_data(self, **kwargs):
        """
        - количество рассылок всего,
        - количество активных рассылок,
        - количество уникальных клиентов для рассылок,
        - три случайные статьи из блога.

        :param kwargs:
        :return:
        """
        context = super().get_context_data(**kwargs)
        # количество рассылок всего
        context["mailings_count"] = len(Mailing.objects.all())
        # количество активных рассылок
        context["mailings_count_active"] = len(Mailing.objects.filter(settings__status=True))

        # количество уникальных клиентов для рассылок
        emails_unique = Client.objects.values('email').annotate(total=Count('id'))
        context["emails_unique"] = emails_unique
        context["emails_unique_count"] = len(emails_unique)
        # три случайные статьи из блога

        # наверняка это можно более оптимально получить, надо спросить как
        # чем весь список статей из базы тянуть
        article_list_len = len(Article.objects.all())

        # article_list_len_2 = Article.objects.Count()

        context["article_list_len"] = article_list_len

        valid_profiles_id_list = Article.objects.values_list('id', flat=True)
        random_profiles_id_list = random.sample(list(valid_profiles_id_list), min(len(valid_profiles_id_list), 3))
        context["random_articles"] = Article.objects.filter(id__in=random_profiles_id_list)

        # def sample(self, population, k, *, counts=None):

        return context
