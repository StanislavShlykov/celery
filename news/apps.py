# from django.apps import AppConfig
#
#
# class NewsConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'news'
#
#
#     def ready(self):
#         from .tasks import send_newsmail
#         from .scheduler import news_send_scheduler
#         print('started')
#
#         news_send_scheduler.add_job(
#             id='send news',
#             func=send_newsmail,
#             trigger='interval',
#             days=7,
#             # seconds=10,
#         )
#         news_send_scheduler.start()