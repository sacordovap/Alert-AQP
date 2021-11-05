from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.shortcuts import redirect, render

from usuarios.models import Incidente, TipoIncidente
from django.core.paginator import Paginator

from django.db.models import Count
from django.urls import reverse
import datetime
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.core import serializers


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

    if request.method == 'POST':
        guardarIncidente(request)
        return redirect("usuarios:historial")

    tipos_delitos = TipoIncidente.objects.all()
    fecha_hoy = datetime.datetime.now()
    data = {
        'fecha_hoy': fecha_hoy,
        'tipos_delitos': tipos_delitos
    }
    return render(request, 'usuarios/reportarIncidente.html', data)


def historial(request):

    usuario_id = 2
    incidentes = Incidente.objects.filter(
        usuario__id=usuario_id).order_by('-id')
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


def guardarIncidente(request):
    titulo = request.POST.get('titulo')
    tipo_incidente_id = request.POST.get('tipo_delito_id')
    descripcion = request.POST.get('descripcion')
    fecha = request.POST.get('fecha')
    hora = request.POST.get('hora')
    titulo = request.POST.get('titulo')
    latitud = request.POST.get('latitud')
    longitud = request.POST.get('longitud')
    direccion = request.POST.get('direccion')
    imagen_url = save_imagen(request)

    usuario = User.objects.get(id=2)
    tipo_incidente = TipoIncidente.objects.get(id=tipo_incidente_id)
    incidente = Incidente.objects.create()
    incidente.tipo_incidente = tipo_incidente
    incidente.usuario = usuario
    incidente.titulo = titulo
    incidente.descripcion = descripcion
    incidente.latitud = latitud
    incidente.longitud = longitud
    incidente.direccion = direccion
    incidente.fecha = fecha
    incidente.hora = hora
    incidente.imagen_video = imagen_url
    incidente.save()

    print("Guardando Datos")


def save_imagen(request):
    if 'imagen' in request.FILES:
        imagen = request.FILES['imagen']
        fss = FileSystemStorage()
        file = fss.save(imagen.name, imagen)
        file_url = fss.url(file)
        return file_url
    return ""


def incidentesCordenadas(request):
    data = Incidente.objects.exclude(Q(latitud__isnull=True) | Q(latitud__exact='')).values()
    return JsonResponse(list(data), safe=False)
