from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Interfaz de administración personalizada para el modelo de usuario personalizado.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_speaker')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'is_speaker', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'organization')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture')}),
        (_('Contact info'), {'fields': ('phone_number', 'organization', 'job_title')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'is_speaker', 'groups', 'user_permissions'),
        }),
        (_('Notifications'), {'fields': ('receive_email_notifications',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_modified')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    
    readonly_fields = ('date_modified',)