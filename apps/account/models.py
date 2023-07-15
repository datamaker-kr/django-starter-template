from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)


class UserManager(BaseUserManager):
    def create(self, **kwargs):
        password = kwargs.pop('password', None)
        user = self.model(**kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        data = {'email': email, 'password': password}
        data.update(kwargs)
        user = self.create(**data)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password=password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    GENDER_CHOICES = [
        ('male', _('남')),
        ('female', _('여')),
    ]

    username = None
    first_name = None
    last_name = None

    email = models.EmailField(_('이메일'), unique=True)
    name = models.CharField(_('이름'), max_length=50)
    objects = UserManager.from_queryset(UserQuerySet)()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        verbose_name = '회원'
        verbose_name_plural = '회원'

    def __str__(self):
        return '[{}] {}'.format(self.pk, self.name)

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return self.name
