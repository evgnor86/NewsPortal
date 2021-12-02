from django.contrib.auth.models import User
from django.db import models


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0)

    def update_rating(self, posts_sum_rate: int, comments_sum_rate: int, posts_comments_sum_rate: int):
        self.rating = posts_sum_rate * 3 + comments_sum_rate + posts_comments_sum_rate
        self.save()


class Category(models.Model):
    name = models.Field(unique=True)


class Post(models.Model):
    POST_TYPES = [
        ('ARTICLE', 'Статья'),
        ('NEWS', 'Новость'),
    ]

    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    type = models.CharField(choices=POST_TYPES, default='NEWS')
    created = models.DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(null=False)
    text = models.CharField(null=False)
    rate = models.FloatField(default=0)

    def like(self):
        self.rate -= 0.1
        self.save()

    def dislike(self):
        self.rate += 0.1
        self.save()


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    text = models.CharField(null=False)
    rate = models.FloatField(default=0)

    def like(self):
        self.rate -= 0.1
        self.save()

    def dislike(self):
        self.rate += 0.1
        self.save()
