from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _

from .forms import CustomUserCreationForm, ProfileUpdateForm

def register(request):
    """
    Vista para el registro de nuevos usuarios.
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, _(f'¡Cuenta creada para {username}! Ahora puedes iniciar sesión.'))
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    """
    Vista para mostrar el perfil del usuario.
    """
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    """
    Vista para actualizar el perfil del usuario.
    """
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _('¡Tu perfil ha sido actualizado!'))
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form
    }
    
    return render(request, 'users/profile_update.html', context)