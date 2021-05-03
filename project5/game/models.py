from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    pass


class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT, related_name='games', blank=False)
    timestamp_save = models.DateTimeField(auto_now_add=True)
    timestamp_won = models.DateTimeField(blank=True, null=True)
    position = models.IntegerField(default=1, blank=False)
    squares = models.CharField(max_length=100, default='0'*100, blank=False)
    keys = models.CharField(max_length = 10, default='0'*10, blank=False)
    
    def __str__(self):
        return f"{self.player}'s game#{self.id}"
