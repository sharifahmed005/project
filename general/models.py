from django.db import models

from account.models import User

# Create your models here.


class Subscriber(models.Model):
    email = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.email


class Message(models.Model):
    expart = models.ForeignKey(
        User, related_name='expart', on_delete=models.CASCADE)
    message = models.TextField()
    seen = models.BooleanField(default=False)
    reply = models.BooleanField(default=False)
    image = models.ImageField(blank=True)
    farmer = models.ForeignKey(
        User, related_name='farmer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.farmer)
