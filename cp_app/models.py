from django.db import models
import hashlib

class User(models.Model):
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=32)

    def save(self, *args, **kwargs):
        passwd_encoded = self.password.encode('utf-8')
        m = hashlib.md5()
        m.update(passwd_encoded)
        self.password = m.hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
