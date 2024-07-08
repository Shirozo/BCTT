from django.db import models
from django.contrib.auth.models import AbstractUser
#0 Create your models here.

class CustomUser(AbstractUser):
    class Designation(models.IntegerChoices):
        MERKADO = 1,
        PEPELITAN = 2 
    
    designation = models.IntegerField(choices=Designation.choices, null=True)