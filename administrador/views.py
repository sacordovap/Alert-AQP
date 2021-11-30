from django.shortcuts import render
from usuarios.models import Incidente, TipoIncidente
from django.core.paginator import Paginator
from django.db.models import Count
import datetime
from django.contrib.auth.decorators import permission_required
# Create your views here.

@permission_required('usuarios.inicio_admin')
def index(request):
    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }
    return render(request, 'administrador/dashboard.html', data)

@permission_required('usuarios.mi_historial_incidentes_admin')
def historial(request):
    return render(request, 'administrador/historial.html')

def mapa(request):

    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }

    return render(request, 'administrador/mapa.html', data)

@permission_required('usuarios.mapa_predictivo_incidentes_admin')
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

@permission_required('usuarios.listado_incidentes_antiguos_admin')
def inicidentes_antiguos(request):
    incidentes = Incidente.objects.order_by('-fecha', '-hora')
    incidentes_paginator = Paginator(incidentes, 5)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)
    data = {
        'page': page,
    }
    return render(request, 'administrador/incidentes_antiguos.html', data)

