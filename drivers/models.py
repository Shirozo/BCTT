from django.db import models

# Create your models here.

class Driver(models.Model):
    class VehicleIdentity(models.TextChoices):
        Cab = 1, "Cab"
        Tricycle = 2, "Tricycle"

    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    qr_code = models.CharField(max_length=100)
    plate_number = models.CharField(max_length=10, null=False, unique=True)
    vhs = models.CharField(choices=VehicleIdentity.choices, null=True, blank=True, max_length=10)
    rate = models.PositiveIntegerField(default=1)
    balance = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"
    
class Operator(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    address = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"