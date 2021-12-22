from django.urls import path

from . import views
app_name = "administrador"
urlpatterns = [
    path('', views.index, name='index'),
    path('usuarios/', views.operaciones_usuario, name='usuarios'),
    path('usuarios-eliminar/', views.operaciones_usuario_eliminar, name='usuarios-eliminar'),
    path('historial/', views.historial, name='historial'),
    path('mapa/', views.mapa, name='mapa'),
    path('mapa-predictivo/', views.mapaPredictivo, name='mapa-predictivo'),
    path('incidentes-reciente/', views.inicidentes_recientes, name='incidentes-recientes'),
    path('incidentes-antiguos/', views.inicidentes_antiguos, name='incidentes-antiguos'),
]

