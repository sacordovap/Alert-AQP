from django.http import HttpResponse
from django.shortcuts import render

from usuarios.models import Incidente, TipoIncidente
from django.core.paginator import Paginator

from django.db.models import Count

import datetime


def index(request):
    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }
    return render(request, 'usuarios/dashboard.html', data)


def mapa(request):

    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total=Count('incidente')).order_by('-total')
    data = {
        'tipo_incidentes': tipo_incidentes
    }

    return render(request, 'usuarios/mapa.html', data)


def mapa2(request):
    return render(request, 'usuarios/mapa2.html')


def incidentes(request):
    incidentes = Incidente.objects.order_by('-fecha', '-hora')
    incidentes_paginator = Paginator(incidentes, 20)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)
    data = {
        'page': page,
    }
    return render(request, 'usuarios/incidentes.html', data)


def reportarIncidente(request):

    fecha_hoy = datetime.datetime.now()
    data = {
        'fecha_hoy': fecha_hoy
    }
    return render(request, 'usuarios/reportarIncidente.html', data)


def historial(request):

    usuario_id = 2
    incidentes = Incidente.objects.filter(
        usuario__id=usuario_id).order_by('-fecha', '-hora')
    incidentes_paginator = Paginator(incidentes, 20)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)
    data = {
        'page': page,
    }
    return render(request, 'usuarios/historial.html', data)


def mapaPredictivo(request):

    fecha_hoy = datetime.datetime.now()  # Returns 2018-01-15 09:00
    data = {
        'fecha_hoy': fecha_hoy
    }
    return render(request, 'usuarios/mapaPredictivo.html', data)
