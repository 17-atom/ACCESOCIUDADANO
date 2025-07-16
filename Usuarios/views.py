from django.shortcuts import render, redirect
from django.contrib.auth.decorators import user_passes_test
from .forms import CrearFormularioUsuario

# Solo permitir acceso al superusuario
@user_passes_test(lambda u: u.is_superuser)
def registrar_usuario(request):
    if request.method == 'POST':
        form = CrearFormularioUsuario(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = CrearFormularioUsuario()

    contexto = {'form': form}
    return render(request, 'Usuarios/registrar_usuario.html', contexto)
