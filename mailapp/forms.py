from django import forms
from django.utils import timezone
from mailapp.models import User, Mail, Mailing, MailingLog


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('username', 'email')


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = '__all__'
        # fields = ('title',
        #           'message',
        #           'status',
        #           'datetime_send',
        #           'user')
        exclude = ('created_at',)

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self.instance)
    #     log.save()
    #
    #     return cleaned_data


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'
