from django import forms

from mailapp.models import User


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        # fields = ('username', 'email')


