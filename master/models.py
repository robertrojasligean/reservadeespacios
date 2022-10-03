from django.db import models

class Estudiante(models.Model):
    codigo = models.CharField(max_length=20)
    nombre = models.CharField(max_length=200)
    carrera = models.CharField(max_length=200)

class Espacio(models.Model):
    nombre = models.CharField(max_length=200)
    tipo = models.CharField(max_length=200)

class EspacioReserva(models.Model):
    espacio = models.ForeignKey(Espacio, on_delete=models.CASCADE)
    horasmaxreserva = models.SmallIntegerField()
    aforo = models.SmallIntegerField()
    habilitado = models.BooleanField()

class Reserva(models.Model):
    espacio_reserva = models.ForeignKey(EspacioReserva, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    hora = models.SmallIntegerField()
    estado = models.CharField(max_length=20)

