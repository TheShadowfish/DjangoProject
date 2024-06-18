from django import forms
from django.forms import BooleanField
from mailapp.models import FreeUser, Client, Mailing, Message, MailingSettings


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class UserForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = FreeUser
        fields = '__all__'
        # fields = ('username', 'email')


class MailingForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        # fields = ('title',
        #           'message',
        #           'status',
        #           'datetime_send',
        #           'user')
        exclude = ('created_at', 'message', 'settings', 'user')
        widgets = {'datetime_send': forms.TextInput(attrs={'type': 'datetime-local'}), }

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self.instance)
    #     log.save()
    #
    #     return cleaned_data


class MailingSettingsModeratorForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = ('status',)
        # fields = ('title',
        #           'message',
        #           'status',
        #           'datetime_send',
        #           'user')
        # exclude = ('created_at', 'message', 'settings', 'user')
        # widgets = {'datetime_send': forms.TextInput(attrs={'type': 'datetime-local'}), }

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self.instance)
    #     log.save()
    #
    #     return cleaned_data


class ClientForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'


class MessageForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Message
        fields = '__all__'


class MailingSettingsForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = MailingSettings
        fields = '__all__'
        widgets = {'datetime_send': forms.TextInput(attrs={'type': 'datetime-local'}), }
        # exclude = ('datetime_send',)
        """
        datetime_send = models.DateTimeField(auto_now_add=True,)
        # раз в день, раз в неделю, раз в месяц
        periodicity = models.PositiveSmallIntegerField(default='1')
        # завершена, запущена
        status = models.BooleanField(default=True, help_text='введите статус (ожидается (запущена) или завершена)')
        active = models.BooleanField(default=True, verbose_name='активность', help_text='запущена ли рассылка сейчас')
        """
