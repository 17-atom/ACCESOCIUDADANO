from django.urls import path
from . import views

app_name = 'App_AccesoCiudadano'

urlpatterns = [
    path('', views.index, name='index'),
    path('registrar_visitante/', views.registrar_visitante, name='registrar_visitante'),
    path('consultar_visitante/', views.consultar_visitante, name='consultar_visitante'),
    path('editar_visitante/<int:id>/', views.editar_visitante, name='editar_visitante'),
    path('eliminar_visitante/<int:id>', views.eliminar_visitante, name='eliminar_visitante'),
    path('registrar_visitas/', views.registrar_visitas, name="registrar_visitas"),
    path('ajax/buscar_visitantes/', views.buscar_visitantes, name="buscar_visitantes"),
    path('reporte/ajax/tabla/', views.ajax_reporte_visitas, name='ajax_reporte_visitas'),
    path('registrar_visitas/registrar_salidas/<int:visita_id>/', views.registrar_salidas, name="registrar_salidas"),
    path('get_responsable/<int:area_id>/', views.get_responsable, name='get_responsable'),
    path('reporte_visitas/', views.reporte_visitas, name="reporte_visitas"),
]