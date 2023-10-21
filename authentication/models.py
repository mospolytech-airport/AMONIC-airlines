from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from authentication.managers import UserManager

from office.models import Office
from role.models import Role


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='E-mail', max_length=500, unique=True)
    first_name = models.CharField(verbose_name='Имя', max_length=50)
    last_name = models.CharField(verbose_name='Фамилия', max_length=150)
    birthday = models.DateField(verbose_name='День рождения', blank=True, null=True)
    is_active = models.BooleanField(verbose_name='Активность', blank=True, default=False)
    is_staff = models.BooleanField(verbose_name='Employee status', default=False, help_text='Определяет, может ли пользователь пользоваться инфраструктурой Employee')
    office = models.ForeignKey(Office, on_delete=models.CASCADE, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)
    login_logout_times = models.JSONField(
        verbose_name='Время входа и выхода',
        blank=True,
        null=True,
    )

    # password по умолчанию в AbstractBaseUser
    # last_login по умолчанию в AbstractBaseUser
    # is_superuser по умолчанию в PermissionsMixin

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    # Модель для ошибок или сбоев
class ErrorLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='error_logs')
    error_msg = models.TextField(verbose_name='Unsuccessful logout reason')
    timestamp = models.DateTimeField(auto_now_add=True)

    