from django.urls import path
# Импортируем созданное нами представление
from .views import NewsList, NewsDetail, PostCreate, PostUpdate, PostDelete, NewsSearch, NewsCreate,content, ArticlesList, ArticlesDetail, sign_me,cat_week


urlpatterns = [
   path('', content),
   path('news/', NewsList.as_view()),
   path('news/sign_me/', sign_me, name='sign_me'),
   path('news/search/', NewsSearch.as_view()),
   path('news/<int:pk>', NewsDetail.as_view(), name = 'post_detail'),
   path('news/create/', PostCreate.as_view(), name='post_create'),
   path('news/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('news/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('news/week/<int:cat_id>/', cat_week, name='cat_week'),
   path('articles/', NewsList.as_view()),
   path('articles/<int:pk>', NewsDetail.as_view(), name='post_detail'),
   path('articles/create/', NewsCreate.as_view(), name='post_create'),
   path('articles/<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
   path('articles/<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),

]