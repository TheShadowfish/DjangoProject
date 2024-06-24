from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView
from django.urls import path, reverse_lazy

from users.apps import UsersConfig
from users.views import RegisterView, email_verification, UserDetailView, UserDeleteView, UserListView, \
    confirm_email, ProfileView, password_recovery, toggle_activity_user

app_name = UsersConfig.name

urlpatterns = [
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path("email-confirm/<str:token>/", email_verification, name='email-confirm'),
    path("users/token_expired.html/", email_verification, name='token_expired'),
    path("users/email_confirmed.html/", email_verification, name='email_confirmed'),
    path("users/confirm_email.html/<str:email>/", confirm_email, name='confirm_email'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('user_list/', UserListView.as_view(), name='user_list'),
    path('user_detail/<int:pk>/', UserDetailView.as_view(), name='user_detail'),


    path('user_activity/<int:pk>/', toggle_activity_user, name='user_activity'),

    path('user_delete/<int:pk>/', UserDeleteView.as_view(), name='user_delete'),

    path("password_recovery/", password_recovery, name='password_recovery'),

    path('password-reset/', PasswordResetView.as_view(template_name='users/password_reset.html',
                                                      email_template_name='users/password_reset_email.html',
                                                      success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),
    path('password-reset/done/', PasswordResetView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html',
                                          success_url=reverse_lazy('users:login')), name='password_reset_confirm'),

]
