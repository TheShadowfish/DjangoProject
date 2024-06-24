from django.urls import path
from django.views.decorators.cache import cache_page

from blogapp.apps import BlogappConfig
from blogapp.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = BlogappConfig.name

urlpatterns = [
    path('article_list', cache_page(60)(ArticleListView.as_view()), name='article_list'),
    path('article_detail/<slug:slug>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article_create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<slug:slug>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<slug:slug>/', ArticleDeleteView.as_view(), name='article_delete'),

]
# path('message_create/', MessageCreateView.as_view(), name='message_create'),
"""
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    
        path("blog", ArticleListView.as_view(), name="blog"),
    path("article/<slug:slug>/", ArticleDetailView.as_view(), name="article_detail"),
    path("article_create/", ArticleCreateView.as_view(), name="article_create"),
    path(
        "article/<slug:slug>/update/", ArticleUpdateView.as_view(), name="article_update"
    ),
    path(
        "article/<slug:slug>/delete/", ArticleDeleteView.as_view(), name="article_delete"
    
    
"""
