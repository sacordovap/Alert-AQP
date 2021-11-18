from django.urls import path

from . import views
app_name = "administrador"
urlpatterns = [
    path('', views.index, name='index'),
    path('historial/', views.historial, name='historial'),
    path('mapa/', views.mapa, name='mapa'),
    path('mapa-predictivo/', views.mapaPredictivo, name='mapa-predictivo'),
]

