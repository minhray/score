from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.

# class User(models.Model):
#     username = models.CharField(default='未知用户', max_length=64)
#     password = models.CharField(max_length=128)

class User(AbstractUser):
    password = models.CharField(max_length=128)


class Client(models.Model):
    user = models.OneToOneField(User, db_constraint=False, related_name='client', on_delete=models.CASCADE, null=True)
    client_num = models.IntegerField(default=0)
    score = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(10000000)])
