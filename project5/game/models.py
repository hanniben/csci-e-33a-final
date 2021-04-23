from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    pass
        

class Square(models.Model):
    col = models.IntegerField(default=0)
    row = models.IntegerField(default=0)
    type = models.IntegerField(default=0)
    visit = models.BooleanField(default=False)

    def __str__(self):
        return f"Game#{self.game} row#{self.row} col#{self.col}"


class Game(models.Model):
    player = models.ForeignKey(User, on_delete=models.PROTECT, related_name='games', blank=False)
    timestamp = models.DateTimeField(blank=True, null=True)
    position = models.CharField(max_length=2, default='A0', blank=False)
    squares = models.CharField(max_length=100, default='0'*100, blank=False)
    
    def __str__(self):
        return f"{self.player}'s game#{self.id}"




class Row(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='grid', blank=False)
    type = models.CharField(max_length=100, default='0'*100, blank=False)

    def __str__(self):
        return f"Game#{self.game.id} row#{self.id}"
