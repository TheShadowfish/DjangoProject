from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blogapp.models import Article


# Create your views here.
class ArticleListView(ListView):
    model = Article


class ArticleDetailView(DetailView):
    model = Article

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()

        return self.object
