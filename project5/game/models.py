from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


# User model
class User(AbstractUser):
    pass


# Game model
class Game(models.Model):
    # User
    player = models.ForeignKey(User, on_delete=models.PROTECT, related_name='games', blank=False)
    # Timestamp of last save
    timestamp_save = models.DateTimeField(auto_now_add=True)
    # Timestamp won
    timestamp_won = models.DateTimeField(blank=True, null=True)
    # Current player position
    position = models.IntegerField(default=1, blank=False)
    # Square statuses
    squares = models.CharField(max_length=100, default='0'*100, blank=False)
    # Key statuses
    keys = models.CharField(max_length = 10, default='0'*10, blank=False)
    # Difficulty mode
    mode = models.BooleanField(default=True, blank=False)
    
    def __str__(self):
        return f"{self.player}'s game#{self.id}"
