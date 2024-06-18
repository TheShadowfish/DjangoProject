from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailapp.forms import UserForm, MailingForm, ClientForm, MessageForm, MailingSettingsForm
from mailapp.models import Client, FreeUser, Mailing, MailingLog, Message, MailingSettings
from mailapp.services import sending
from mailapp.utils.utils import get_info_and_send, select_mailings


# from django.apps.config import models.Mail

class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    login_url = "users:login"
    # redirect_field_name = "login"


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('mailapp:mail_list')


# class MailDetailView(DetailView):
#     model = Mail


class UserListView(LoginRequiredMixin, ListView):
    model = FreeUser


class UserCreateView(LoginRequiredMixin, CreateView):
    model = FreeUser
    form_class = UserForm
    success_url = reverse_lazy('mailapp:user_list')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = FreeUser
    form_class = UserForm
    success_url = reverse_lazy('mailapp:user_list')


class UserDetailView(LoginRequiredMixin, DetailView):
    model = FreeUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mailing_list'] = Mailing.objects.all()
        context['mailing_list'] = Mailing.objects.filter(user=self.object)
        return context


class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = FreeUser
    success_url = reverse_lazy('mailapp:user_list')


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


class MailFormsetMixin:

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
        # self.object = form.save()

        mailing = form.save()
        if mailing.message is None:
            message = Message.objects.create(title=f"{mailing.title} - first ",
                                             body=f"{mailing.message_in} - first creation")
            message.save()
            mailing.message = message
            print(f'Сохранение сообщения {mailing.message}')
            mailing.save()
            print('mailing.save()')
        else:
            message = Message.objects.get(id=mailing.message_id)

        if mailing.settings is None:
            settings = MailingSettings.objects.create()
            settings.save()
            mailing.settings = settings
            print(f'Сохранение настроек {mailing.settings}')
            settings.save()
            # print('settings.save()')
        # else:
        # settings = MailingSettings.objects.get(id=mailing.settings_id)

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


class MailingCreateView(LoginRequiredMixin, MailFormsetMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailapp:mailing_list')  # object.pk


class MailingUpdateView(LoginRequiredMixin, MailFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailapp:mailing_list')


class MailingDetailView(LoginRequiredMixin, DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = MailingLog.objects.filter(mailing=self.object)
        context['clients'] = Client.objects.filter(mailing=self.object)
        context['message'] = Message.objects.get(id=self.object.message_id)
        context['settings'] = MailingSettings.objects.get(id=self.object.settings_id)
        return context


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')


class MessageSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:settings_list')

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
        return context


class MailingSettingsUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailapp:settings_list')


class MailingSettingsListView(LoginRequiredMixin, ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
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
