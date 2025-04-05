from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Event, Category, Registration, Session
from .forms import EventForm, RegistrationForm, EventSearchForm

def event_list(request):
    """
    Vista para listar todos los eventos.
    """
    form = EventSearchForm(request.GET)
    events = Event.objects.filter(status=Event.EventStatus.PUBLISHED)
    
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        category_id = form.cleaned_data.get('category')
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        
        if keyword:
            events = events.filter(
                Q(title__icontains=keyword) | Q(description__icontains=keyword)
            )
        
        if category_id:
            events = events.filter(category__id=category_id)
        
        if start_date:
            events = events.filter(start_date__gte=start_date)
        
        if end_date:
            events = events.filter(end_date__lte=end_date)
    
    # Paginar los resultados
    paginator = Paginator(events, 9)  # 9 eventos por página
    page = request.GET.get('page')
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    # Obtener próximos eventos destacados
    featured_events = Event.objects.filter(
        status=Event.EventStatus.PUBLISHED,
        is_featured=True,
        start_date__gt=timezone.now()
    ).order_by('start_date')[:3]
    
    context = {
        'events': events,
        'featured_events': featured_events,
        'search_form': form,
        'categories': Category.objects.all()
    }
    
    return render(request, 'events/event_list.html', context)

def event_detail(request, slug):
    """
    Vista para ver los detalles de un evento.
    """
    event = get_object_or_404(Event, slug=slug, status=Event.EventStatus.PUBLISHED)
    sessions = event.sessions.all().order_by('start_time')
    user_registered = False
    
    if request.user.is_authenticated:
        user_registered = Registration.objects.filter(
            user=request.user,
            event=event
        ).exists()
    
    context = {
        'event': event,
        'sessions': sessions,
        'user_registered': user_registered
    }
    
    return render(request, 'events/event_detail.html', context)

@login_required
def event_register(request, slug):
    """
    Vista para registrarse en un evento.
    """
    event = get_object_or_404(Event, slug=slug, status=Event.EventStatus.PUBLISHED)
    
    # Verificar si el usuario ya está registrado
    existing_registration = Registration.objects.filter(
        user=request.user,
        event=event
    ).first()
    
    if existing_registration:
        messages.info(request, _('You are already registered for this event.'))
        return redirect('event_detail', slug=event.slug)
    
    # Verificar si hay plazas disponibles
    if event.max_attendees and event.registered_count >= event.max_attendees:
        messages.error(request, _('Sorry, this event is fully booked.'))
        return redirect('event_detail', slug=event.slug)
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.user = request.user
            registration.event = event
            registration.save()
            
            messages.success(request, _('You have successfully registered for this event!'))
            return redirect('event_detail', slug=event.slug)
    else:
        form = RegistrationForm()
    
    context = {
        'event': event,
        'form': form
    }
    
    return render(request, 'events/event_register.html', context)

@login_required
def registration_cancel(request, registration_id):
    """
    Vista para cancelar una inscripción a un evento.
    """
    registration = get_object_or_404(
        Registration,
        id=registration_id,
        user=request.user
    )
    
    # No permitir cancelar si el evento ya pasó
    if registration.event.is_past:
        messages.error(request, _('You cannot cancel a registration for a past event.'))
        return redirect('user_registrations')
    
    if request.method == 'POST':
        registration.status = Registration.RegistrationStatus.CANCELLED
        registration.save()
        messages.success(request, _('Your registration has been cancelled.'))
        return redirect('user_registrations')
    
    context = {
        'registration': registration
    }
    
    return render(request, 'events/registration_cancel.html', context)

@login_required
def user_registrations(request):
    """
    Vista para ver todas las inscripciones del usuario.
    """
    registrations = Registration.objects.filter(user=request.user).order_by('-registration_date')
    
    context = {
        'registrations': registrations
    }
    
    return render(request, 'events/user_registrations.html', context)

def category_detail(request, slug):
    """
    Vista para ver todos los eventos de una categoría.
    """
    category = get_object_or_404(Category, slug=slug)
    events = Event.objects.filter(
        category=category,
        status=Event.EventStatus.PUBLISHED
    ).order_by('start_date')
    
    # Paginar los resultados
    paginator = Paginator(events, 9)  # 9 eventos por página
    page = request.GET.get('page')
    
    try:
        events = paginator.page(page)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        events = paginator.page(paginator.num_pages)
    
    context = {
        'category': category,
        'events': events
    }
    
    return render(request, 'events/category_detail.html', context)

@login_required
def session_detail(request, session_id):
    """
    Vista para ver los detalles de una sesión.
    """
    session = get_object_or_404(Session, id=session_id)
    
    # Verificar si el usuario está registrado para el evento
    user_registered = False
    if request.user.is_authenticated:
        user_registered = Registration.objects.filter(
            user=request.user,
            event=session.event,
            status__in=[Registration.RegistrationStatus.CONFIRMED, Registration.RegistrationStatus.ATTENDED]
        ).exists()
    
    context = {
        'session': session,
        'user_registered': user_registered
    }
    
    return render(request, 'events/session_detail.html', context)