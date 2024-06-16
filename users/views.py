import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User, UserToken


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token

        user_token = UserToken.objects.create(token=token, user=user)
        user_token.save()

        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email-confirm/{token}/'
        # print(url)
        send_mail(
            subject='Подтверждение почты',
            message=f'Привет, перейди по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        # print(f'Отправлено {EMAIL_HOST_USER} to {user.email}')
        return super().form_valid(form)


def email_verification(request, token):
    user = get_object_or_404(User)
    this_user_token = get_object_or_404(UserToken, user=user, token=token)

    if this_user_token.created_at < timezone.now() - timezone.timedelta(hours=1):
        this_user_token.delete()
        return render(request, 'users/token_expired.html')
    else:
        this_user_token.delete()
        user.is_active = True
        user.save()
        return render(request, 'users/email_confirmed.html')

    #
    # user = get_object_or_404(User, token=token)
    # user.is_active = True
    # user.save()
    # return redirect(reverse('users:login'))


def token_expired(request):
    return render(request, 'users/token_expired.html')


def email_confirmed(request):
    return render(request, 'users/email_confirmed.html')
