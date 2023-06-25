from celery import shared_task
import time
from news.models import Category
from django.core.mail import send_mail
from another_shop.settings import DEFAULT_FROM_EMAIL
from django.template.loader import render_to_string

@shared_task
def hello():
    time.sleep(10)
    print("Hello, world!")


@shared_task
def send_week_email():
    categories = Category.objects.all()
    for categ in categories:
        subs_email = []
        subs_users = categ.users.all()
        for s_users in subs_users:
            subs_email.append(s_users.email)
        send_mail(
            subject=f'Статьи по теме {categ.cat_name} за неделю',
            message=None,
            from_email=DEFAULT_FROM_EMAIL,
            recipient_list=subs_email,
            html_message=f'''<h3>Пройдите по ссылке, чтобы посмотреть все статьи за неделю <a href='http://127.0.0.1:8000/news/week/{categ.id}'>ссылка</a></h3>''',
            fail_silently=True
        )

@shared_task
def mail_new(categories, news):
    subs_email = []
    for categ in categories:
        subs_users = categ.users.all()
        for s_users in subs_users:
            subs_email.append(s_users.email)
    html_content = render_to_string('sign/hello.html', {'news': news})
    send_mail(
        subject=f'новая статья {news.post_name}',
        message=None,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=subs_email,
        html_message=html_content,
        fail_silently=True
    )