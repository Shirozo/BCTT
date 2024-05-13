from django.db import models

# Create your models here.
    
class Operator(models.Model):
    operator_first_name = models.CharField(max_length=50, null=False)
    operator_last_name = models.CharField(max_length=50, null=False)
    operator_address = models.CharField(max_length=100, null=False)

    def __str__(self) -> str:
        return f"{self.operator_last_name}, {self.operator_first_name}"

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
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.last_name}, {self.first_name}"
    