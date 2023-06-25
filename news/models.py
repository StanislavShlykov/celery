from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.

name = [
    (False, 'Статья'),
    (True, 'Новость')
]

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        rating1 = 0
        rating2 = 0
        rating3 = 0
        au_us_id = self.user_id
        posts_ex = Post.objects.exclude(author_id=self.id)
        for i in self.post_set.all().values():
            rating1 += i['post_rating']*3
        for i in self.post_set.all():
            for j in i.comment_set.all().values():
                rating2 += j['com_rating']
        for i in posts_ex:
            for m in i.comment_set.all().filter(user_id = au_us_id).values():
                rating3 += m['com_rating']
        self.rating = rating1+rating2+rating3
        self.save()

    def __str__(self):
        return f'{self.name}'


class Category(models.Model):
    cat_name = models.CharField(max_length=50, unique=True)
    users = models.ManyToManyField(User, through='UserCategory')

    def __str__(self):
        return f'{self.cat_name}'


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.BooleanField(default=False, choices=name)  # False = статья, можно переделать, если будет больше вариантов
    time_in = models.DateTimeField(auto_now_add=True)
    post_name = models.CharField(max_length=100)
    post_text = models.TextField(default="Тут должен быть идиотский контент, а будет абракадабра, для проверки задания: дурак ываываываф идиот ыафыаываывфа мудак ываф ываф ывп фывп фвап фвп выа фывп фыва выа ыфвп выа фыв афвыа ывф.")
    post_rating = models.IntegerField(default=0)
    post_chek = models.BooleanField(default=False)

    category = models.ManyToManyField(Category, through='PostCategory')

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        if self.post_rating > 0:
            self.post_rating -= 1
            self.save()

    def preview(self):
        return self.post_text[:20] + '...'



    def __str__(self):
        return f'{self.post_name.title()} {self.time_in}: {self.preview()}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class UserCategory(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    com_date = models.DateTimeField(auto_now_add=True)
    com_rating = models.IntegerField(default=0)

    def like(self):
        self.com_rating += 1
        self.save()

    def dislike(self):
        if self.com_rating > 0:
            self.com_rating -= 1
            self.save()
