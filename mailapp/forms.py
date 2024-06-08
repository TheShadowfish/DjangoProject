from django import forms

from mailapp.models import User, Mail, Mailing


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('username', 'email')


class MailForm(forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'


class MailingForm(forms.ModelForm):
    class Meta:
        model = Mailing
        fields = ('title',
                  'message',
                  'status',
                  'datetime_send',
                  'user')
