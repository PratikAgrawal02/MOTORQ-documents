# documents/models.py

from django.db import models

class User(models.Model):
    mobile_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords

    def __str__(self):
        return self.mobile_number
