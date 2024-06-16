import secrets

from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView, UpdateView, DetailView, DeleteView

from config.settings import EMAIL_HOST_USER
from mailapp.models import Mailing
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User, UserToken


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:confirm_email')

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
    # user = get_object_or_404(User)
    # message = Message.objects.get(pk=mailing_item.message_id)
    # mail_title = mailing_item.message.title
    # mail_body = mailing_item.message.body
    # mail_list = Client.objects.filter(mailing=mailing_item)

    this_user_token = get_object_or_404(UserToken, token=token)
    user = this_user_token.user

    if this_user_token.created_at < timezone.now() - timezone.timedelta(minutes=45):
        user.delete()
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


def confirm_email(request):
    return render(request, 'users/confirm_email.html')


class UserListView(ListView):
    model = User


# class UserCreateView(CreateView):
#     model = User
#     form_class = UserForm
#     success_url = reverse_lazy('users:user_list')


class UserUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user_list')


class UserDetailView(DetailView):
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['mailing_list'] = Mailing.objects.all()
        context['mailing_list'] = Mailing.objects.filter(user=self.object)
        return context


class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('users:user_list')
