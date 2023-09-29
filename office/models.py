from django.db import models

from authentication.models import User

class Office(models.Model):
    title = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)