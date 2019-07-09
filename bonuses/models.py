from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    amount_of_bonuses = models.DecimalField(verbose_name='Bonuses', max_digits=13, decimal_places=0, default=0)


