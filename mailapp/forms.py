from django import forms
from django.forms import BooleanField
from mailapp.models import User, Mail, Mailing


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
        model = User
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
        exclude = ('created_at',)

    # def clean(self):
    #     cleaned_data = self.cleaned_data
    #     log = MailingLog.objects.create(log_text=f'Change parameters {timezone.now()}', mailing=self.instance)
    #     log.save()
    #
    #     return cleaned_data


class MailForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Mail
        fields = '__all__'
