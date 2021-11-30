# Generated by Django 3.2.9 on 2021-11-30 02:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0012_alter_incidente_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incidente',
            options={'permissions': (('inicio', 'Acceso a la pantalla de inicio de usuario ciudadano'), ('listado_incidentes', 'Retorna el listado de Incidentes'), ('reportar_incidentes', 'Puede reportar incidentes'), ('mi_historial_incidentes', 'Listado de mi historial de incidentes'), ('mapa_incidentes', 'Visualización de Mapa de incidentes'), ('mapa_predictivo_incidentes', 'Visualización de Mapa predictivo'), ('inicio_admin', '(Admin) Acceso a la pantalla de inicio de Administrador'), ('listado_incidentes_recientes_admin', '(Admin) Retorna el listado de Incidentes Recientes'), ('listado_incidentes_antiguos_admin', '(Admin) Retorna el listado de Incidentes Antiguos'), ('mi_historial_incidentes_admin', '(Admin) Listado de mi historial de incidentes atendidos'), ('mapa_incidentes_admin', '(Admin) Visualización de Mapa de incidentes'), ('mapa_predictivo_incidentes_admin', '(Admin) Visualización de Mapa predictivo'))},
        ),
    ]
