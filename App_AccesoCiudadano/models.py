from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

# 1. Modelo para Responsables de Área (empleados de la entidad)
class ResponsableArea(models.Model):
    dni = models.CharField(max_length=20, unique=True, verbose_name="DNI")
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    activo = models.BooleanField(default=True)  # Para deshabilitar sin eliminar

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"

# 2. Modelo para Áreas de la entidad
class Area(models.Model):
    nombre_area = models.CharField(max_length=100, verbose_name="Área")
    responsable_actual = models.ForeignKey(
        ResponsableArea,
        on_delete=models.SET_NULL,
        null=True,
        related_name='areas_actuales'
    )

    def __str__(self):
        return self.nombre_area

# 3. Historial de cambios de responsables (auditoría)
class HistorialResponsable(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='historial')
    responsable = models.ForeignKey(ResponsableArea, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(default=timezone.now)
    fecha_fin = models.DateField(null=True, blank=True)
    cambiado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.area.nombre_area}: {self.responsable} ({self.fecha_inicio} a {self.fecha_fin or 'Actual'})"

# 4. Visitantes externos (personas que ingresan a la entidad)
class Visitante(models.Model):
    dni = models.CharField(
        max_length=8,
        unique=True,
        verbose_name="DNI",
        validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe tener exactamente 8 dígitos numéricos')]
    )
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} (DNI: {self.dni})"

    dni = models.CharField(max_length=8, unique=True, verbose_name="DNI")
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    fecha_registro = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} {self.apellidos} (DNI: {self.dni})"

# 5. Registro de visitas (entradas/salidas)
class Visita(models.Model):
    visitante = models.ForeignKey(Visitante, on_delete=models.CASCADE, related_name='visitas')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    motivo = models.TextField(verbose_name="Motivo de la visita")
    fecha_entrada = models.DateTimeField(auto_now_add=True)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)  # Recepcionista

    def __str__(self):
        return f"Visita de {self.visitante} a {self.area.nombre_area}"

    class Meta:
        ordering = ['-fecha_entrada']