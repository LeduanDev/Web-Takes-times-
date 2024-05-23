from django.contrib import admin
from .models import Categoria, Maquina, Estudio, Actividad, Tipo, Area, User

# Registra tus modelos aquí
admin.site.register(Categoria)
admin.site.register(Maquina)
admin.site.register(Estudio)
admin.site.register(Actividad)
admin.site.register(Tipo)
admin.site.register(Area)
admin.site.register(User)
