from django.shortcuts import render, HttpResponse
from django.template.loader import render_to_string
from news.models import Post, Category, Author
from news.filters import PostFilter
from django.urls import reverse_lazy
from news.forms import PostForm
from django.core.mail import send_mail
from another_shop.settings import DEFAULT_FROM_EMAIL
import datetime


def send_email():
    categories = Category.objects.all()
    for categ in categories:
        subs_email = []
        subs_users = categ.users.all()
        for s_users in subs_users:
            subs_email.append(s_users.email)
        # html_content = render_to_string('sign/hello.html', {'cat': categ})
        send_mail(
            subject=f'Статьи по теме {categ.cat_name} за неделю',
            message=None,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=subs_email,
            html_message=f'''<h3>Пройдите по ссылке, чтобы посмотреть все статьи за неделю <a href='http://127.0.0.1:8000/news/week/{categ.id}'>ссылка</a></h3>''',
            fail_silently=True
        )

