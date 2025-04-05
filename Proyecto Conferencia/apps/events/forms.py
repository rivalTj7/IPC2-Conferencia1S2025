from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Event, Session, Registration

class EventForm(forms.ModelForm):
    """
    Formulario para crear y editar eventos.
    """
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'category', 'location',
            'start_date', 'end_date', 'image', 'registration_required',
            'max_attendees', 'is_featured'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError(_('End date must be after start date.'))
        
        return cleaned_data

class SessionForm(forms.ModelForm):
    """
    Formulario para crear y editar sesiones.
    """
    class Meta:
        model = Session
        fields = [
            'title', 'description', 'event', 'start_time',
            'end_time', 'room', 'speakers'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        event = cleaned_data.get('event')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError(_('End time must be after start time.'))
        
        if event and start_time and (start_time < event.start_date or start_time > event.end_date):
            raise forms.ValidationError(_('Session must be within event dates.'))
        
        if event and end_time and (end_time > event.end_date):
            raise forms.ValidationError(_('Session must end before event ends.'))
        
        return cleaned_data

class RegistrationForm(forms.ModelForm):
    """
    Formulario para registrarse en un evento.
    """
    class Meta:
        model = Registration
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'placeholder': _('Any special requirements or comments?')})
        }

class EventSearchForm(forms.Form):
    """
    Formulario para buscar eventos.
    """
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Search by title or description')})
    )
    category = forms.ChoiceField(
        required=False,
        choices=[(None, _('All Categories'))]
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        category_choices = [(c.id, c.name) for c in Category.objects.all()]
        self.fields['category'].choices = [(None, _('All Categories'))] + category_choices