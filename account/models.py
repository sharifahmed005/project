from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    FARMAR = 'FARMAR'
    AGRICULTURERIST = 'AGRICULTURERIST'
    VATONARIS = 'VATONARIS'

    USER_TYPE = [
        (FARMAR, 'FARMAR'),
        (AGRICULTURERIST, 'AGRICULTURERIST'),
        (VATONARIS, 'VATONARIS'),
    ]
    user_type = models.CharField(
        choices=USER_TYPE, default=FARMAR, max_length=50)
    image = models.ImageField(default="default.png")
    about = models.TextField(null=True, blank=True)
