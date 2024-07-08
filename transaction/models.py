from django.db import models
from drivers.models import Driver

# Create your models here.
class Transaction(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    transact_date = models.DateTimeField(auto_now=True)


class DriverScan(models.Model):
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE, null=False)
    endpoint = models.CharField(max_length=50, null=True)
    scanDate = models.DateTimeField(auto_now=True)
    action = models.CharField(max_length=10, null=True, blank=True)
    show = models.BooleanField(default=True)