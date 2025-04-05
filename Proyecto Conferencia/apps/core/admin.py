from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage, FAQ, Sponsor

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_at', 'read')
    list_filter = ('read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'
    
    def has_add_permission(self, request):
        # No se deberían agregar mensajes de contacto manualmente
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Solo el superusuario puede eliminar mensajes
        return request.user.is_superuser

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)
    search_fields = ('question', 'answer')

@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'website', 'active')
    list_filter = ('level', 'active')
    search_fields = ('name', 'description')