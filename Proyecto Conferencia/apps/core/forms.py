from django import forms
from django.utils.translation import gettext_lazy as _

from .models import ContactMessage

class ContactForm(forms.ModelForm):
    """
    Formulario para mensajes de contacto.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'message': forms.Textarea(attrs={'rows': 5}),
        }