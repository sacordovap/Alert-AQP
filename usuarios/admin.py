from django.contrib import admin

from usuarios.models import Incidente, TipoIncidente

# Register your models here.
admin.site.register(Incidente)
admin.site.register(TipoIncidente)