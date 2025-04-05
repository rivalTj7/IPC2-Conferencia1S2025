from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .forms import ContactForm
from .models import FAQ, Sponsor
from apps.events.models import Event
from apps.speakers.models import SpeakerProfile

def home(request):
    """
    Vista para la página principal.
    """
    # Obtener eventos próximos
    upcoming_events = Event.objects.filter(
        status=Event.EventStatus.PUBLISHED,
        start_date__gt=timezone.now()
    ).order_by('start_date')[:6]
    
    # Obtener eventos destacados
    featured_events = Event.objects.filter(
        status=Event.EventStatus.PUBLISHED,
        is_featured=True
    ).order_by('start_date')[:3]
    
    # Obtener ponentes destacados
    featured_speakers = SpeakerProfile.objects.filter(featured=True)[:4]
    
    # Obtener patrocinadores activos
    sponsors = Sponsor.objects.filter(active=True).order_by('-level')
    
    context = {
        'upcoming_events': upcoming_events,
        'featured_events': featured_events,
        'featured_speakers': featured_speakers,
        'sponsors': sponsors
    }
    
    return render(request, 'core/home.html', context)

def about(request):
    """
    Vista para la página Acerca de.
    """
    return render(request, 'core/about.html')

def contact(request):
    """
    Vista para la página de contacto.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your message has been sent. We will contact you soon!'))
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    
    return render(request, 'core/contact.html', context)

def faq(request):
    """
    Vista para la página de preguntas frecuentes.
    """
    faqs = FAQ.objects.all()
    
    context = {
        'faqs': faqs
    }
    
    return render(request, 'core/faq.html', context)

def sponsors(request):
    """
    Vista para la página de patrocinadores.
    """
    platinum_sponsors = Sponsor.objects.filter(level=Sponsor.SponsorLevel.PLATINUM, active=True)
    gold_sponsors = Sponsor.objects.filter(level=Sponsor.SponsorLevel.GOLD, active=True)
    silver_sponsors = Sponsor.objects.filter(level=Sponsor.SponsorLevel.SILVER, active=True)
    bronze_sponsors = Sponsor.objects.filter(level=Sponsor.SponsorLevel.BRONZE, active=True)
    
    context = {
        'platinum_sponsors': platinum_sponsors,
        'gold_sponsors': gold_sponsors,
        'silver_sponsors': silver_sponsors,
        'bronze_sponsors': bronze_sponsors
    }
    
    return render(request, 'core/sponsors.html', context)