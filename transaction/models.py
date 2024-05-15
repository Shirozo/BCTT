from django.db import models
from drivers.models import Driver

# Create your models here.
class Transaction(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    amount = models.PositiveIntegerField(default=1)
    transact_date = models.DateTimeField(auto_now=True)


class DriverScan(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    amount = models.PositiveIntegerField(default=0)
    endpoint = models.CharField(max_length=50)
    scanDate = models.DateTimeField(auto_now=True)