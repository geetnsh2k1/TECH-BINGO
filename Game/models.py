from django.db import models
from Profile.models import Profile
from Question.models import Question

# Create your models here.
class Game(models.Model):
    
    Start = models.DateTimeField(auto_now_add=True)
    
    Player = models.OneToOneField(Profile, on_delete=models.CASCADE, null=False)
    
    Questions = models.ManyToManyField(Question, related_name='Questions', blank=True)
    
    Matrix = models.TextField(default="2-d matrix")
    
    Completed = models.CharField(max_length=20, blank=True)
    
    Current = models.CharField(max_length=10, default="BINGO")
    
    End = models.DateTimeField(null=True)
    
    Penalty = models.IntegerField(default=0)
    
    Status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.Player.User.username + " - " + self.Current