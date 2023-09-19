from django.db import models
from authentication.models import User


class Role(models.Model):
    title = models.CharField(max_length=200)
    role_id = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)