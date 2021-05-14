from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ip_address = models.GenericIPAddressField(verbose_name="آدرس آیپی", null=True)