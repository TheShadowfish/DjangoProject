from django.urls import path

from blogapp.apps import BlogappConfig
from blogapp.views import ArticleListView

app_name = BlogappConfig.name

urlpatterns = [
    path('article_list', ArticleListView.as_view(), name='article_list'),

]
# path('message_create/', MessageCreateView.as_view(), name='message_create'),
"""
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
"""
