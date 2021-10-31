from django.urls import path

from . import views
app_name = "usuarios"
urlpatterns = [
    path('', views.index, name='index'),
    path('incidentes/', views.incidentes, name='incidentes'),
    path('incidentes/reportar/', views.reportarIncidente, name='reportarIncidente'),
    path('incidentes/mapa/', views.mapa, name='mapa'),
    path('incidentes/mapa2/', views.mapa2, name='mapa2'),
    path('mapa-predictivo/', views.mapaPredictivo, name='mapaPredictivo'),
    path('historial/', views.historial, name='historial'),
]
