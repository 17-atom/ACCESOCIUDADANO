from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Visitante, Area, Visita
from .forms import VisitanteForm, EditarVisitanteForm
from datetime import date
from django.utils import timezone
from django.contrib import messages
from django.http import Http404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    # Obtener las visitas activas desde la otra vista
    visitas_activas = Visita.objects.filter(fecha_salida__isnull=True).order_by('-fecha_entrada')
    
    # Aquí deberías también obtener las otras estadísticas que usas en el template
    contexto = {
        'visitas': visitas_activas,  # Cambiado a 'visitas' para coincidir con el template
        'total_clientes': Visitante.objects.count(),  # Ejemplo, ajusta según tu modelo
        'visitas_hoy': Visita.objects.filter(fecha_entrada__date=date.today()).count(),
        'entradas_hoy': Visita.objects.filter(fecha_entrada__date=date.today()).count(),
        'salidas_hoy': Visita.objects.filter(fecha_salida__date=date.today()).count(),
        'en_curso': Visita.objects.filter(fecha_salida__isnull=True).count()
    }
    return render(request, 'App_AccesoCiudadano/index.html', contexto)

@login_required
def registrar_visitante(request):
    if request.method != 'POST':
        formulario = VisitanteForm()
    else:
        formulario = VisitanteForm(request.POST)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Visitante guardado correctamente.')
            return redirect('App_AccesoCiudadano:registrar_visitante')
    
    visitantes = Visitante.objects.all().order_by('-id')
    contexto = {
        'list_visitante':visitantes,
        'formulario':formulario,
    }
    return render(request,'App_AccesoCiudadano/registrar_visitante.html', contexto)

def ajax_reporte_visitas(request):
    rpt_visitas = Visita.objects.select_related('visitante', 'area', 'area__responsable_actual').order_by('-fecha_entrada')
    return render(request, 'partials/tabla_reporte.html', {'rpt_visitas': rpt_visitas})

def consultar_visitante(request):
    nombre = request.GET.get("nombre_visitante", "")
    
    if nombre:
        resultados = Visitante.objects.filter(nombre__icontains=nombre)
        if not resultados.exists():
            messages.error(request, "Visitante consultado no existe")
    else:
        resultados = Visitante.objects.all()

    formulario = VisitanteForm()  # <--- importante: crea el formulario vacío

    contexto = {
        'list_visitante': resultados,
        'formulario': formulario  # <--- pásalo a la plantilla
    }
    return render(request, 'App_AccesoCiudadano/registrar_visitante.html', contexto)

@login_required
def editar_visitante(request, id):
    try:
        visitante = Visitante.objects.get(pk=id)
    except Visitante.DoesNotExist:
        raise Http404("El visitante no existe")
                
    if request.method == 'POST':
        formulario = EditarVisitanteForm(request.POST, instance=visitante)
        if formulario.is_valid():
            formulario.save()
            return redirect('App_AccesoCiudadano:registrar_visitante')
    else:
        formulario = EditarVisitanteForm(instance=visitante)

    contexto = {
        'formulario':formulario,
        'visitante':visitante,
    }
    return render(request, 'App_AccesoCiudadano/editar_visitante.html', contexto)

def eliminar_visitante(request,id):
    visitante = get_object_or_404(Visitante, pk=id)
    visitante.delete()
    messages.success(request, 'Visitante eliminado correctamente')
    return redirect('App_AccesoCiudadano:registrar_visitante')

@login_required
def buscar_visitantes(request):
    term = request.GET.get('term', '')
    visitantes = Visitante.objects.filter(nombre__icontains=term)[:20]

    data = []
    for visitante in visitantes:
        data.append({
            'id': visitante.id,
            'text': f"{visitante.nombre} {visitante.apellidos} - DNI: {visitante.dni}"
        })
    return JsonResponse({'results': data})

@login_required
@require_http_methods(["GET", "POST"])
def registrar_visitas(request):
    if request.method == 'POST':
        visitante_id = request.POST.get('visitante').title()
        area_id = request.POST.get('area').title()
        motivo = request.POST.get('motivo', '').strip().capitalize()

        if visitante_id and area_id and motivo:
            try:
                visitante = Visitante.objects.get(id=visitante_id)
                area = Area.objects.get(id=area_id)
                Visita.objects.create(
                    visitante=visitante,
                    area=area,
                    motivo=motivo,
                    fecha_entrada=timezone.now()
                )
                messages.success(request, "✅ Visita registrada exitosamente.")
                return redirect('App_AccesoCiudadano:registrar_visitas')
            except (Visitante.DoesNotExist, Area.DoesNotExist):
                messages.error(request, "❌ El visitante o área seleccionada no existe.")
        else:
            messages.error(request, "⚠️ Todos los campos son obligatorios.")

    visitas = Visita.objects.all()

    context = {
        'visitas': visitas,
        #'visitantes': Visitante.objects.all(),
        'areas': Area.objects.all(),
        
    }
    return render(request, 'App_AccesoCiudadano/registrar_visitas.html', context)

def registrar_salidas(request, visita_id):
    visita = get_object_or_404(Visita, pk=visita_id)
    
    if request.method == 'POST':
        if not visita.fecha_salida:
            visita.fecha_salida = timezone.now()
            visita.save()
            messages.success(request, f"Salida registrada para {visita.visitante.nombre}")
        else:
            messages.warning(request, f"La salida ya estaba registrada a las {visita.fecha_salida.strftime('%H:%M')}")
        
        return redirect('App_AccesoCiudadano:registrar_visitas')
    
    messages.error(request, "Método no permitido")
    return redirect('App_AccesoCiudadano:registrar_visitas')


def get_responsable(request, area_id):
    try:
        area = Area.objects.select_related('responsable_actual').get(id=area_id)
        responsable = area.responsable_actual
        if responsable:
            data = {
                'responsable': {
                    'nombre': responsable.nombre,
                    'apellidos': responsable.apellidos,
                }
            }
        else:
            data = {'responsable': {'nombre': 'Sin', 'apellidos': 'asignar'}}
        return JsonResponse(data)
    except Area.DoesNotExist:
        return JsonResponse({'error': 'Área no encontrada'}, status=404)

def reporte_visitas(request):
    rpt_visitas = Visita.objects.all().order_by('fecha_salida')

    contexto = {
        'rpt_visitas':rpt_visitas,
    }

    return render(request, 'App_AccesoCiudadano/reporte_visitas.html', contexto)