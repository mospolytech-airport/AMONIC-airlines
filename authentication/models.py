from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from authentication.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-mail', max_length=500, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активность', blank=True, default=False)
    is_staff = models.BooleanField(verbose_name='Employee status', default=False, help_text='Определяет, может ли пользователь пользоваться инфраструктурой Employee')
    # password по умолчанию в AbstractBaseUser
    # last_login по умолчанию в AbstractBaseUser
    # is_superuser по умолчанию в PermissionsMixin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    