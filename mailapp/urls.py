from django.urls import path
from .views import MailListView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, \
    MailingListView, MailingCreateView, MailingUpdateView, MailingListViewSend, MailingDeleteView, MailCreateView, \
    MailUpdateView, MailDeleteView, MailingDetailView

from mailapp.apps import MailappConfig
app_name = MailappConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='main'),
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
    path('mail_list/', MailListView.as_view(), name='mail_list'),
    path('mail_create/', MailCreateView.as_view(), name='mail_create'),
    path('mail_update/<int:pk>/', MailUpdateView.as_view(), name='mail_update'),
    path('mail_delete/<int:pk>/', MailDeleteView.as_view(), name='mail_delete'),



]
