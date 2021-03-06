from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta

from apps.account.models import Account, UserConfirmCode
from apps.account.utils import generate_token


@shared_task
def send_email_on_registration(domain, uid):
    user = Account.objects.get(id=uid)
    token = generate_token.make_token(user)

    email_body = render_to_string('accounts/activation.html', context={'domain': domain, 'user': user, 'token': token})

    send_mail(
        'Activate your account',
        'message',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=email_body
    )


@shared_task
def send_email_on_login(domain, uid,code):
    user = Account.objects.get(id=uid)

    email_body = render_to_string('accounts/confirm_message.html', context={'domain': domain, 'user': user, 'code' : code})

    send_mail(
        'Login account',
        'message',
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=email_body
    )


@shared_task
def check_code_status():
    for user_code in UserConfirmCode.objects.all():
        time_now = timezone.now()
        if time_now > user_code.sended + timedelta(minutes=5):
            user_code.delete()