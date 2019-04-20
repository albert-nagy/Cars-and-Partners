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
    created_at = UnixTimeStampField(auto_now_add=True, blank=False)
    modify_at = UnixTimeStampField(auto_now=True, blank=False)
    deleted_at = UnixTimeStampField(default=0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        try:
            self.id = Partner.objects.latest('id').id +1
        except Partner.DoesNotExist:
            self.id = 1
        super().save(*args, **kwargs)