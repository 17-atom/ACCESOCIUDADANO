from django import forms
from .models import Visita, Visitante
from django.core.validators import RegexValidator

class VisitaForm(forms.ModelForm):
    class Meta:
        model = Visita
        fields = ['visitante', 'area', 'motivo']  # fecha_entrada y registrado_por se autocompletan
        widgets = {
            'motivo': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'visitante': forms.Select(attrs={'class': 'form-control'}),
            'area': forms.Select(attrs={'class': 'form-control', 'onchange': 'cargarResponsable()'}),
        }

class VisitanteForm(forms.ModelForm):
    dni = forms.CharField(
        max_length=8,
        validators=[RegexValidator(regex=r'^\d{8}$', message='El DNI debe tener exactamente 8 dígitos numéricos')],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'DNI',
            'pattern': '[0-9]{8}',  # Validación adicional en HTML
            'title': 'Ingrese 8 dígitos numéricos'
        })
    )

    class Meta:
        model = Visitante
        fields = ['dni', 'nombre', 'apellidos']
        labels = {
            'dni': 'DNI',
            'nombre': 'Nombres',
            'apellidos': 'Apellidos',
        }
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellidos'}),
        }
    
    #metodo para guardar valores de tipo title()
    def clean(self):
        cleaned_data = super().clean()
        nombre = cleaned_data.get('nombre')
        apellidos = cleaned_data.get('apellidos')
        if nombre:
            cleaned_data['nombre'] = nombre.title()
        if apellidos:
            cleaned_data['apellidos'] = apellidos.title()

        return cleaned_data

class EditarVisitanteForm(forms.ModelForm):
    class Meta:
        model = Visitante
        fields = ['dni', 'nombre', 'apellidos']
        labels = {
            'dni':'DNI',
            'nombre': 'Nombres',
            'apellidos': 'Apellidos',
        }
        widgets = {
            'dni': forms.TextInput(attrs={'class':'form-control', 'placeholder':'DNI'}),
            'nombre': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Nombre'}),
            'apellidos': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Apellidos'}),
        }

    def __init__(self, *args, **kwargs):
        super(EditarVisitanteForm, self).__init__(*args, **kwargs)
        self.fields['dni'].disabled = True  # <-- Esto desactiva la edición del campo DNI