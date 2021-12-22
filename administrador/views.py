from django.shortcuts import render
from usuarios.models import Incidente, TipoIncidente, EstadoIncidente
from django.core.paginator import Paginator
from django.db.models import Count
import datetime
from django.contrib.auth.decorators import permission_required
# Create your views here.
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
import uuid
from administrador.models import AtenderIncidente
from django.contrib.auth.models import Group, User


@permission_required('usuarios.inicio_admin')
def operaciones_usuario(request):

    if request.method == 'POST':
        guardarUsuario(request)
        return redirect("administrador:usuarios")

    #usuarios = User.objects.filter(groups__name__in=['Administrador', 'Ciudadano'])
    usuarios = User.objects.all()
    usuarios_paginator=Paginator(usuarios, 5)
    page_num=request.GET.get('page')
    page=usuarios_paginator.get_page(page_num)

    roles = Group.objects.filter(name__in=['Administrador', 'Ciudadano'])

    fecha_hoy=datetime.datetime.now()
    data={
        'page': page,
        'fecha_hoy': fecha_hoy,
        'roles': roles
    }
    return render(request, 'administrador/usuarios.html', data)
@permission_required('usuarios.inicio_admin')
def operaciones_usuario_eliminar(request):

    eliminarUsuario(request)
 
    return redirect("administrador:usuarios")
 
@permission_required('usuarios.inicio_admin')
def index(request):
    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total = Count('incidente')).order_by('-total')
    data={
        'tipo_incidentes': tipo_incidentes
    }
    return render(request, 'administrador/dashboard.html', data)

@permission_required('usuarios.mi_historial_incidentes_admin')
def historial(request):
    current_user = request.user
    usuario_id = current_user.id
    incidentes = AtenderIncidente.objects.filter(
        usuario__id = usuario_id).order_by('-fecha', '-hora')

    incidentes_paginator=Paginator(incidentes, 5)
    page_num=request.GET.get('page')
    page=incidentes_paginator.get_page(page_num)

    data={
        'page': page,
    }


    return render(request, 'administrador/historial.html', data)
@permission_required('usuarios.mapa_incidentes_admin')
def mapa(request):

    tipo_incidentes = TipoIncidente.objects.all().annotate(
        total = Count('incidente')).order_by('-total')
    data={
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

@permission_required('usuarios.listado_incidentes_recientes_admin')
def inicidentes_recientes(request):

    if request.method == 'POST':
        guardarAtenderIncidente(request)
        return redirect("administrador:historial")

    incidentes = Incidente.objects.filter(
        estado = EstadoIncidente.SIN_ATENDER).order_by('-fecha', '-hora')
    incidentes_paginator=Paginator(incidentes, 5)
    page_num=request.GET.get('page')
    page=incidentes_paginator.get_page(page_num)

    fecha_hoy=datetime.datetime.now()
    data={
        'page': page,
        'fecha_hoy': fecha_hoy
    }
    return render(request, 'administrador/incidentes_recientes.html', data)

@permission_required('usuarios.listado_incidentes_antiguos_admin')
def inicidentes_antiguos(request):
    incidentes = AtenderIncidente.objects.order_by('-fecha', '-hora')

    incidentes_paginator = Paginator(incidentes, 5)
    page_num = request.GET.get('page')
    page = incidentes_paginator.get_page(page_num)

    data = {
        'page': page,
    }
    return render(request, 'administrador/incidentes_antiguos.html', data)


def guardarAtenderIncidente(request):
    observaciones = request.POST.get('observaciones')
    incidente_id = request.POST.get('incidente_id')
    fecha = request.POST.get('fecha')
    hora = request.POST.get('hora')
    falsa_alarma = request.POST.get('falsa_alarma')
    if(falsa_alarma == 'on'):
        falsa_alarma = True
    else:
        falsa_alarma = False

    imagen_url = save_imagen(request)

    print("HOLA", falsa_alarma)
    usuario = request.user
    incidente = Incidente.objects.get(id=incidente_id)
    atenderIncidente = AtenderIncidente.objects.create()
    atenderIncidente.incidente = incidente
    atenderIncidente.usuario = usuario
    atenderIncidente.observaciones = observaciones
    atenderIncidente.fecha = fecha
    atenderIncidente.hora = hora
    atenderIncidente.imagen_video = imagen_url
    atenderIncidente.false_alarma = falsa_alarma
    atenderIncidente.save()
    print("Observaciones: ", observaciones)
    incidente.estado = EstadoIncidente.ARCHIVADO
    incidente.save()
    print("Guardando Datos")


def save_imagen(request):
    if 'imagen' in request.FILES:
        imagen = request.FILES['imagen']
        fss = FileSystemStorage()

        file = fss.save(nombre_unico_imagen(imagen), imagen)
        file_url = fss.url(file)
        return file_url
    return "/media/default.jpg"
def nombre_unico_imagen(imagen):
    ext = imagen.name.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename

def guardarUsuario(request):
    
    name = request.POST.get('name')
    surname = request.POST.get('surname')
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    rol_id = request.POST.get('rol_id')
    
    
    try:
        u = User.objects.get(username = username)
       
    except User.DoesNotExist:
        group = Group.objects.get(id=rol_id)
        user = User.objects.create()
        user.first_name = name
        user.last_name = surname
        user.email = email
        user.username = username
        user.set_password(password)
        user.save()
        user.groups.add(group)
        print("Guardando Datos", rol_id, username, password)
        
@permission_required('usuarios.inicio_admin')
def eliminarUsuario(request):
    id = request.GET.get('id')
    u = User.objects.get(id = id)
    if u.username != "administrador" and u.username!="ciudadano":
        u.delete()
    
    
    print("Eliminando", u)
