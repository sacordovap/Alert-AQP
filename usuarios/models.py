from django.db import models
from django.conf import settings
import datetime
# Create your models here.

class EstadoIncidente(models.IntegerChoices):
    SIN_ATENDER = 0, 'Sin atender'
    POR_ATENDER = 1, 'Por Atender'
    ARCHIVADO = 2, 'Incidente Archivado'
class TipoIncidente(models.Model):
    titulo = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.titulo

class Incidente(models.Model):
    titulo = models.CharField(max_length=100, null=True)
    descripcion = models.CharField(max_length=255, null=True)
    imagen_video = models.CharField(max_length=255, null=True)
    latitud = models.CharField(max_length=100, null=True)
    longitud = models.CharField(max_length=100, null=True)
    hora = models.TimeField(default=datetime.datetime.now, null=True)
    fecha = models.DateField(default=datetime.date.today, null=True)
    direccion = models.CharField(max_length=255, null=True)
    false_alarma = models.BooleanField(default=False, null=True)
    estado = models.IntegerField(default= EstadoIncidente.SIN_ATENDER, choices=EstadoIncidente.choices, null=True)
    usuario = models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    tipo_incidente = models.ForeignKey(TipoIncidente, on_delete=models.SET_NULL, null=True)
    
    class Meta:
        permissions = (("inicio","Acceso a la pantalla de inicio de usuario ciudadano"), ("listado_incidentes", "Retorna el listado de Incidentes"), ("reportar_incidentes", "Puede reportar incidentes"), ("mi_historial_incidentes","Listado de mi historial de incidentes"), ("mapa_incidentes","Visualización de Mapa de incidentes"), ("mapa_predictivo_incidentes","Visualización de Mapa predictivo"),  )
    
    def __str__(self):
        return self.titulo
