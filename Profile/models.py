from django.db import models
from django.contrib.auth.models import User as Usr
from django.core.validators import RegexValidator
from multiselectfield import MultiSelectField

# Create your models here.
def profile_file_path(instance, filename):
    return '/'.join(['Profile', instance.User.username, 'Profile_Picture',  filename])

class Profile(models.Model):
    
    Created = models.DateTimeField(auto_now_add=True)
    
    User = models.OneToOneField(Usr, unique=True, on_delete=models.CASCADE, null=False)
    
    Phone = models.IntegerField(null=False)
    
    College = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.User.username