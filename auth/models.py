from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-mail', max_length=500, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    birthday = models.DateField(label='День рождения')
    is_active = models.BooleanField(label='Актвность')
    # password по умолчанию в AbstractBaseUser
    # last_login по умолчанию в AbstractBaseUser
    # is_superuser по умолчанию в PermissionsMixin
