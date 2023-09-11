# documents/models.py

from django.db import models
from django.contrib.auth.models import User

class Person(models.Model):
    mobile_number = models.CharField(max_length=10, unique=True)
    password = models.CharField(max_length=100)  # Store hashed passwords

    def __str__(self):
        return self.mobile_number
    
class Document(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)