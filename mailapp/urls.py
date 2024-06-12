from django.urls import path
from .views import ClientListView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingListViewSend, MailingDeleteView, ClientCreateView, \
    ClientUpdateView, ClientDeleteView, MailingDetailView, mailing_send, MessageListView, MessageUpdateView, \
    MessageCreateView

from mailapp.apps import MailappConfig
app_name = MailappConfig.name



urlpatterns = [
    path('', ClientListView.as_view(), name='main'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),
    path('mailing_list/', MailingListView.as_view(), name='mailing_list'),
    path('mailing_list_send/', MailingListViewSend.as_view(), name='mailing_list_send'),
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),
    path('mailing_update/<int:pk>/', MailingUpdateView.as_view(), name='mailing_update'),
    path('mailing_delete/<int:pk>/', MailingDeleteView.as_view(), name='mailing_delete'),
    path('mailing_detail/<int:pk>/', MailingDetailView.as_view(), name='mailing_detail'),
    path('mail_list/', ClientListView.as_view(), name='mail_list'),
    path('mail_create/', ClientCreateView.as_view(), name='mail_create'),
    path('mail_update/<int:pk>/', ClientUpdateView.as_view(), name='mail_update'),
    path('mail_delete/<int:pk>/', ClientDeleteView.as_view(), name='mail_delete'),
    path('mailing_send/<int:pk>/', mailing_send, name='mailing_send'),
    path('message_list/', MessageListView.as_view(), name='message_list'),
    path('message_create/', MessageCreateView.as_view(), name='message_create'),
    path('message_update/<int:pk>/', MessageUpdateView.as_view(), name='message_update'),



]
