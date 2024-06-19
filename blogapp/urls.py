from django.urls import path

from blogapp.apps import BlogappConfig
from blogapp.views import ArticleListView, ArticleDetailView, ArticleCreateView, ArticleUpdateView, ArticleDeleteView

app_name = BlogappConfig.name

urlpatterns = [
    path('article_list', ArticleListView.as_view(), name='article_list'),
    path('article_detail/<int:pk>/', ArticleDetailView.as_view(), name='article_detail'),
    path('article_create/', ArticleCreateView.as_view(), name='article_create'),
    path('article_update/<int:pk>/', ArticleUpdateView.as_view(), name='article_update'),
    path('article_delete/<int:pk>/', ArticleDeleteView.as_view(), name='article_delete'),

]
# path('message_create/', MessageCreateView.as_view(), name='message_create'),
"""
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    
    
    
    
"""
