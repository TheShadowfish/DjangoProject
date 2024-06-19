from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from blogapp.forms import ArticleForm
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


class ArticleCreateView(LoginRequiredMixin, CreateView):
    # PermissionRequiredMixin  permission_required = "article.add_article"
    model = Article

    form_class = ArticleForm

    success_url = reverse_lazy("blogapp:article_list")

    login_url = "users:login"
    redirect_field_name = "login"

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_article = form.save()
    #         new_article.slug = slugify(new_article.name)
    #         new_article.save()
    #     return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    # permission_required = "article.update_article" PermissionRequiredMixin

    # success_url = reverse_lazy('article:blog')

    login_url = "users:login"
    redirect_field_name = "login"

    # def form_valid(self, form):
    #     if form.is_valid():
    #         new_article = form.save()
    #         new_article.slug = slugify(new_article.name)
    #         new_article.save()
    #     return super().form_valid(form)

    def get_success_url(self):
        return reverse("blogapp:article_detail", args=[self.kwargs.get("pk")])


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy("blogapp:article_list")
    # permission_required = "article.delete_article" PermissionRequiredMixin

    login_url = "users:login"
    redirect_field_name = "login"
