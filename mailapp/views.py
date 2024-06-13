from django.forms import inlineformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from mailapp.forms import UserForm, MailingForm, ClientForm, MessageForm, MailingSettingsForm
from mailapp.models import Client, User, Mailing, MailingLog, Message, MailingSettings
from mailapp.services import sending


# from django.apps.config import models.Mail

class ClientListView(ListView):
    model = Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('mailapp:mail_list')


class ClientDeleteView(DeleteView):
    model = Client
    success_url = reverse_lazy('mailapp:mail_list')


# class MailDetailView(DetailView):
#     model = Mail


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mailing_list'] = Mailing.objects.all()
        context['mailing_list'] = Mailing.objects.filter(user=self.object)
        return context


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('mailapp:user_list')


class MailingListView(ListView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['only_send'] = False
        return context


class MailingListViewSend(ListView):
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

        if mailing.settings is None:
            settings = MailingSettings.objects.create(mailing=mailing)
            settings.save()
            mailing.settings = settings
            print(f'Сохранение настроек {mailing.settings}')
            settings.save()
            print('settings.save()')

        log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=mailing)
        log.save()
        print('log.save()')

        formset = self.get_context_data()['formset']
        if formset.is_valid():
            formset.instance = mailing
            formset.save()

        # print(f"message.id= {message.id}, message= {message}, mailing.message_id={mailing.message_id}")
        # redirect_url = reverse('mailapp:message_update', args=[message.id])

        redirect_url = reverse('mailapp:message_settings_update', args=[mailing.message_id])
        # { % if mailing_item.message_id == object.id %}
        self.success_url = redirect_url

        return super().form_valid(form)


class MailingCreateView(MailFormsetMixin, CreateView):
    model = Mailing
    form_class = MailingForm

    success_url = reverse_lazy('mailapp:mailing_list')  # object.pk

    # def get_success_url(self):
    #     print(f"1 {self}")
    #     print(f"2 {self.args}")
    #     print(f"3 {[self.kwargs.get('pk')]}")
    #     print(f"4 {self.message_id}")
    #     return reverse('mailapp:message_update', args=[self.object.message_id])

    # context['message'] = Message.objects.filter(id=self.object.message_id)


class MailingUpdateView(MailFormsetMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    success_url = reverse_lazy('mailapp:mailing_list')

    # def save(self, commit=True):
    #     instance = super(Form, self).save(commit=False)
    #     instance.flag1 = 'flag1' in self.cleaned_data['multi_choice']  # etc
    #     if commit:
    #         instance.save()
    #     return instance


class MailingDeleteView(DeleteView):
    model = Mailing
    success_url = reverse_lazy('mailapp:mailing_list')


class MailingDetailView(DetailView):
    model = Mailing

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logs'] = MailingLog.objects.filter(mailing=self.object)
        context['clients'] = Client.objects.filter(mailing=self.object)
        context['message'] = Message.objects.filter(id=self.object.message_id)
        return context


class MessageCreateView(CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')


class MessageUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')


class MessageSettingsUpdateView(UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('mailapp:message_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailing'] = Message.objects.filter(message_id=self.object.id)
        return context

    def form_valid(self, form):
        # self.object = form.save()
        mailing = self.get_context_data()['mailing']

        print(f"message.id= {mailing.id}, message= {mailing}, mailing.message_id={mailing.message_id}")
        # redirect_url = reverse('mailapp:message_update', args=[message.id])

        redirect_url = reverse('mailapp:settings_update', args=[mailing.settings_id])

        # { % if mailing_item.message_id == object.id %}
        self.success_url = redirect_url

        return super().form_valid(form)


class MessageListView(ListView):
    model = Message

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        return context


class MailingSettingsUpdateView(UpdateView):
    model = MailingSettings
    form_class = MailingSettingsForm
    success_url = reverse_lazy('mailapp:settings_list')


class MailingSettingsListView(ListView):
    model = MailingSettings

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mailings'] = Mailing.objects.all()
        return context


def mailing_send(request, pk):
    mailing_item = get_object_or_404(Mailing, pk=pk)

    print("mailing_send")

    try:
        sending(mailing_item)
    except Exception as e:
        print(e)
    else:
        mailing_item.status = True
        mailing_item.save()

    print(mailing_item)
    print(mailing_item.status)
    return redirect(reverse('mailapp:mailing_list'))
