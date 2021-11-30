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
    incidentes = Incidente.objects.order_by('-fecha', '-hora')
    incidentes_paginator = Paginator(incidentes, 5)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)
    data = {
        'page': page,
    }
    return render(request, 'administrador/incidentes_recientes.html', data)

def inicidentes_antiguos(request):
    incidentes = Incidente.objects.order_by('-fecha', '-hora')
    incidentes_paginator = Paginator(incidentes, 5)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)
    data = {
        'page': page,
    }
    return render(request, 'administrador/incidentes_antiguos.html', data)

