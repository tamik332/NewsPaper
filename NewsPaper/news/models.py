from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.FloatField(default=0.0)

    def update_rating(self):
        articles_rating = self.posts.aggregate(models.Sum("rating"))['rating__sum'] or 0
        comments_rating = self.user.comments.aggregate(models.Sum("rating"))['rating__sum'] or 0
        article_comments_rating = (self.posts
                                   .filter(author__user__comments__isnull=False)
                                   .aggregate(models.Sum('author__user__comments__rating'))['author__user__comments__rating__sum'] or 0)

        total_rating = articles_rating * 3 + comments_rating + article_comments_rating
        self.rating = total_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)


class PostCategory(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='posts')
    post_type = models.CharField(max_length=7, choices=[('article', 'Статья'), ('news', 'Новость')])
    create_at = models .DateTimeField(auto_now_add=True)
    category = models.ManyToManyField(Category, through=PostCategory)
    title = models.CharField(max_length=255)
    content = models.TextField()
    rating = models.FloatField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.content[:124] + '...'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    create_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0.0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
