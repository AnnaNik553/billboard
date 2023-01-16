from django.template.loader import render_to_string
from django.core.mail import send_mail

from users.models import User


def weekly_newsletter():
    # выбираем email пользователей
    users_email = [user.email for user in User.objects.all() if user.email]

    # письмо преобразуем в строку
    letter = render_to_string('posts/letter.html')

    send_mail(subject='Billboard - новости',
              message='Billboard - новости',
              from_email='Billboard <matoko18@yandex.ru>',
              recipient_list=users_email,
              fail_silently=True,
              html_message=letter)
