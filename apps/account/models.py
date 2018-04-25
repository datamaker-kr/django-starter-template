from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    first_name = None
    last_name = None

    name = models.CharField('이름', max_length=50)

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원'
