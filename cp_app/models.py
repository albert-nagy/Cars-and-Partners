from django.db import models
import hashlib

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=16)

    def save(self, *args, **kwargs):        
        self.password = hashlib.md5.new(self.field).digest()
        super().save(*args, **kwargs)
