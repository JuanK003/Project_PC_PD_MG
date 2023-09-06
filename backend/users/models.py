from django.db import models

# Create your models here.
class Users(models.Model):
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=150)
    email = models.EmailField()

class Torneos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_torneo = models.CharField(max_length=100)
    deporte = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    # Colección de equipos (referencia a la colección Equipos)
    equipos = models.ManyToManyField('Equipos', related_name='torneos')
    id_usuario = models.ForeignKey(Users, on_delete=models.CASCADE)

class Equipos(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    # Colección de jugadores
    jugadores = models.ManyToManyField('Jugadores', related_name='equipos')

class Jugadores(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_jugador = models.CharField(max_length=100)
    numero_identificador = models.CharField(max_length=100)
    posicion = models.CharField(max_length=100)
    numero = models.IntegerField()

class Playoffs(models.Model):
    id = models.AutoField(primary_key=True)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    # Colección de fases
    fases = models.ManyToManyField('Fases', related_name='playoffs')

class Fases(models.Model):
    nombre_fase = models.CharField(max_length=100)
    # Colección de partidos
    partidos = models.ManyToManyField('Partidos', related_name='fases')

class Partidos(models.Model):
    equipo_1 = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='partidos_equipo_1')
    equipo_2 = models.ForeignKey(Equipos, on_delete=models.CASCADE, related_name='partidos_equipo_2')
    resultado = models.CharField(max_length=100)