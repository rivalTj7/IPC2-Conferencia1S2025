from django import forms
from django.utils.translation import gettext_lazy as _

from .models import SpeakerProfile, Presentation

class SpeakerProfileForm(forms.ModelForm):
    """
    Formulario para crear y editar perfiles de ponentes.
    """
    class Meta:
        model = SpeakerProfile
        fields = [
            'headline', 'bio_extended', 'specializations',
            'website', 'twitter_handle', 'linkedin_url', 
            'github_username', 'speaking_experience',
            'languages', 'presentation_topics'
        ]
        widgets = {
            'bio_extended': forms.Textarea(attrs={'rows': 6}),
            'speaking_experience': forms.Textarea(attrs={'rows': 4}),
            'presentation_topics': forms.Textarea(attrs={'rows': 4}),
            'twitter_handle': forms.TextInput(attrs={'placeholder': '@username'}),
        }

class PresentationForm(forms.ModelForm):
    """
    Formulario para crear y editar presentaciones.
    """
    class Meta:
        model = Presentation
        fields = [
            'title', 'event_name', 'date', 'description',
            'video_url', 'slides_url'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class SpeakerSearchForm(forms.Form):
    """
    Formulario para buscar ponentes.
    """
    keyword = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('Search by name or bio')})
    )
    specialization = forms.ChoiceField(
        required=False,
        choices=[(None, _('All Specializations'))]
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Specialization
        specialization_choices = [(s.id, s.name) for s in Specialization.objects.all()]
        self.fields['specialization'].choices = [(None, _('All Specializations'))] + specialization_choices