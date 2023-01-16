from django.core.mail import send_mail
from django.shortcuts import redirect, render

from users.forms import CreationForm


def send_msg(login, email):
    subject = 'Регистрация прошла успешно'
    body = f"""Ваш аккаунт успешно зарегистрирован на сайте Yatube!

    Чтобы войти в свой аккаунт используйте логин: {login}.

    С уважением, команда Yatube.

    """
    send_mail(subject, body, 'adminyatube@yandex.ru', [email, ])


def sing_up(request):
    form = CreationForm(request.POST or None)
    if form.is_valid():
        send_msg(form.cleaned_data['username'],
                 form.cleaned_data['email'])
        form.save()
        return redirect('posts:index')
    return render(request, 'users/signup.html', context={'form': form})
