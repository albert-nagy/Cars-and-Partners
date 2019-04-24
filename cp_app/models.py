from django.db import models
from django.contrib.postgres.fields import ArrayField
from unixtimestampfield.fields import UnixTimeStampField
from django.contrib.auth.models import User

# Create your models here.
class Partner(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=160, blank=False)
    city = models.CharField(max_length=100, blank=False)
    address = models.CharField(max_length=200, blank=False)
    company_name = models.CharField(max_length=160, blank=False)
    cars = ArrayField(
        models.IntegerField(), blank=True, default=list
        )
    created_at = UnixTimeStampField(
        auto_now_add=True,
        use_numeric=True,
        round_to=3,
        blank=False
        )
    modify_at = UnixTimeStampField(
        auto_now=True,
        use_numeric=True,
        round_to=3,
        blank=False
        )
    deleted_at = UnixTimeStampField(
        default=0,
        use_numeric=True,
        round_to=3
        )

    def __str__(self):
        return self.name

class Car(models.Model):
    id = models.IntegerField(default=0, primary_key=True)
    user = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    average_fuel = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
        )
    delegation_starting = UnixTimeStampField( use_numeric=True, default=0)
    delegation_ending = UnixTimeStampField(use_numeric=True, default=0)
    driver = models.CharField(max_length=160)
    owner = models.CharField(max_length=160)

    TYPE_CHOICES = (
        ('pr', 'private'),
        ('co', 'company'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='co')

    partners = ArrayField(
        models.IntegerField(), blank=True, default=list
        )

    created_at = UnixTimeStampField(
        auto_now_add=True,
        use_numeric=True,
        round_to=3,
        blank=False
        )
    modify_at = UnixTimeStampField(
        auto_now=True,
        use_numeric=True,
        round_to=3,
        blank=False
        )
    deleted_at = UnixTimeStampField(
        default=0,
        use_numeric=True,
        round_to=3
        )

    def __str__(self):
        return str(self.id)