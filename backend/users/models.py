from django.db import models

class User(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    email = models.EmailField()

class Tournament(models.Model):
    name = models.CharField(max_length=100)
    sport = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    teams = models.ManyToManyField('Team', related_name='tournaments')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

class Team(models.Model):
    name = models.CharField(max_length=100)
    players = models.ManyToManyField('Player', related_name='teams')

class Player(models.Model):
    player_name = models.CharField(max_length=100)
    identifier_number = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    number = models.IntegerField()

class Playoff(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    phases = models.ManyToManyField('Phase', related_name='playoffs')

class Phase(models.Model):
    phase_name = models.CharField(max_length=100)
    matches = models.ManyToManyField('Match', related_name='phases')

class Match(models.Model):
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='matches_team_2')
    result = models.CharField(max_length=100)
