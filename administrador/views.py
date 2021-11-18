from django.shortcuts import render
from usuarios.models import Incidente, TipoIncidente
from django.core.paginator import Paginator
from django.db.models import Count
import datetime
# Create your views here.
def index(request):
    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }
    return render(request, 'administrador/dashboard.html', data)

def historial(request):
    return render(request, 'administrador/historial.html')

def mapa(request):

    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }

    return render(request, 'administrador/mapa.html', data)


def mapaPredictivo(request):

    fecha_hoy = datetime.datetime.now()  # Returns 2018-01-15 09:00
    data = {
        'fecha_hoy': fecha_hoy
    }
    
    return render(request, 'administrador/mapaPredictivo.html', data)

def inicidentes_recientes(request):
    return render(request, 'administrador/incidentes_recientes.html')

def inicidentes_antiguos(request):
    return render(request, 'administrador/incidentes_antiguos.html')

