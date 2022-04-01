from django.db import models
from account.models import User
# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=255)
    details = models.TextField()
    image = models.ImageField(upload_to='blog', default='720x400.png')
    author = models.ForeignKey(
        User, related_name='blog', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title


class Comments(models.Model):
    blog = models.ForeignKey(Blog, related_name='blog',
                             on_delete=models.CASCADE)
    comment = models.TextField()
    commenter = models.ForeignKey(
        User, related_name='commenter', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.comment
