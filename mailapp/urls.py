from django.urls import path
from .views import MailListView, UserListView, UserCreateView

from mailapp.apps import MailappConfig
app_name = MailappConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='main'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_create/', UserCreateView.as_view(), name='user_create'),

]
