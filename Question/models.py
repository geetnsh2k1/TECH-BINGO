import uuid
from django.db import models

# Create your models here.
class Question(models.Model):
    
    Id = models.UUIDField(primary_key=True, default = uuid.uuid4, editable = False)
    
    Problem = models.TextField(blank=False)
    
    Answer = models.CharField(max_length=100, blank=False)
    
    def __str__(self):
        return str(self.Id)