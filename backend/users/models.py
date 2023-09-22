from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    email = models.EmailField()

class Tournaments(models.Model):
    id = models.AutoField(primary_key=True)
    name_tournament = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    # Collection of teams (reference to the Teams collection)
    teams = models.ManyToManyField('Teams', related_name='tournaments')
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE)

class Teams(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # Collection of players
    players = models.ManyToManyField('Players', related_name='teams')

class Players(models.Model):
    id = models.AutoField(primary_key=True)
    player_name = models.CharField(max_length=100)
    identifier_number = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    number = models.IntegerField()

class Playoffs(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    # Collection of phases
    phases = models.ManyToManyField('Phases', related_name='playoffs')

class Phases(models.Model):
    phase_name = models.CharField(max_length=100)
    # Collection of matches
    matches = models.ManyToManyField('Matches', related_name='phases')

class Matches(models.Model):
    team_1 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='matches_team_1')
    team_2 = models.ForeignKey(Teams, on_delete=models.CASCADE, related_name='matches_team_2')
    result = models.CharField(max_length=100)
