from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UserDetailView, UserUpdateView, UserDeleteView, UserListView

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("users/token_expired.html/", email_verification, name='token_expired'),
    path("users/email_confirmed.html/", email_verification, name='email_confirmed'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('user_update/<int:pk>/', UserUpdateView.as_view(), name='user_update'),
    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

]
