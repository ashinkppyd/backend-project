from django.contrib.auth.models import AbstractUser
from django.db import models

class UserAccount(AbstractUser):
    role = models.CharField(max_length=20, default="user")
    is_email_verified = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)



