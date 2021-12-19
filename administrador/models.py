from django.db import models
from django.conf import settings
import datetime

from usuarios.models import Incidente
# Create your models here.

class AtenderIncidente(models.Model):
    
    hora = models.TimeField(default=datetime.datetime.now, null=True)
    fecha = models.DateField(default=datetime.date.today, null=True)
    observaciones = models.CharField(max_length=255, null=True)
    imagen_video = models.CharField(max_length=255, null=True)
    false_alarma = models.BooleanField(default=False, null=True)
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    incidente = models.ForeignKey(
        Incidente, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo
