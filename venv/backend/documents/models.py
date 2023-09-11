# documents/models.py

from django.db import models
from django.contrib.auth.models import User

    
class Document(models.Model):
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shared_with = models.ManyToManyField(User, related_name='shared_documents', null=True)

    def __str__(self):
        return self.name

    
class DocumentSharing(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    has_access = models.BooleanField(default=True)