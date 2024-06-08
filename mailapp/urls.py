from django.urls import path
from .views import MailListView, UserListView, UserCreateView, UserDetailView, UserUpdateView, UserDeleteView, \
    MailingListView, MailingCreateView

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
    path('mailing_create/', MailingCreateView.as_view(), name='mailing_create'),



]
