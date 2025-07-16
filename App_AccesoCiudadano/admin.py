from django.contrib import admin
from .models import ResponsableArea, Area, HistorialResponsable, Visitante, Visita

@admin.register(ResponsableArea)
class ResponsableAreaAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellidos', 'telefono', 'email', 'activo')
    search_fields = ('dni', 'nombre', 'apellidos')
    list_filter = ('activo',)

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('nombre_area', 'responsable_actual')
    search_fields = ('nombre_area',)
    list_filter = ('responsable_actual',)

@admin.register(HistorialResponsable)
class HistorialResponsableAdmin(admin.ModelAdmin):
    list_display = ('area', 'responsable', 'fecha_inicio', 'fecha_fin', 'cambiado_por')
    list_filter = ('fecha_inicio', 'fecha_fin', 'area')
    search_fields = ('area__nombre_area', 'responsable__nombre', 'responsable__apellidos')

@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('dni', 'nombre', 'apellidos', 'fecha_registro')
    search_fields = ('dni', 'nombre', 'apellidos')

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ('visitante', 'area', 'motivo', 'fecha_entrada', 'fecha_salida', 'registrado_por')
    list_filter = ('fecha_entrada', 'fecha_salida', 'area')
    search_fields = ('visitante__nombre', 'visitante__apellidos', 'area__nombre_area')
