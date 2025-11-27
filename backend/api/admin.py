from django.contrib import admin
from .models import Locais, Responsaveis, Ambientes, Sensores, Historico

admin.site.register(Locais)
admin.site.register(Responsaveis)
admin.site.register(Ambientes)
admin.site.register(Sensores)
admin.site.register(Historico)

