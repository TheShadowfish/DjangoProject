from django import forms

from blogapp.models import Article
from mailapp.forms import StyleFormMixin


class ArticleForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Article
        fields = (
            "title",
            "body",
            "image",
        )
