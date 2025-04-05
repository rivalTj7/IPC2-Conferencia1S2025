from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import SpeakerProfile, Specialization, Presentation
from .forms import SpeakerProfileForm, PresentationForm, SpeakerSearchForm
from apps.events.models import Session

def speaker_list(request):
    """
    Vista para listar todos los ponentes.
    """
    form = SpeakerSearchForm(request.GET)
    speakers = SpeakerProfile.objects.all()
    
    if form.is_valid():
        keyword = form.cleaned_data.get('keyword')
        specialization_id = form.cleaned_data.get('specialization')
        
        if keyword:
            speakers = speakers.filter(
                Q(user__first_name__icontains=keyword) | 
                Q(user__last_name__icontains=keyword) |
                Q(headline__icontains=keyword) |
                Q(bio_extended__icontains=keyword)
            )
        
        if specialization_id:
            speakers = speakers.filter(specializations__id=specialization_id)
    
    # Destacar los ponentes destacados primero
    speakers = speakers.order_by('-featured', 'user__last_name', 'user__first_name')
    
    # Paginar los resultados
    paginator = Paginator(speakers, 12)  # 12 ponentes por página
    page = request.GET.get('page')
    
    try:
        speakers = paginator.page(page)
    except PageNotAnInteger:
        speakers = paginator.page(1)
    except EmptyPage:
        speakers = paginator.page(paginator.num_pages)
    
    context = {
        'speakers': speakers,
        'search_form': form,
        'specializations': Specialization.objects.all()
    }
    
    return render(request, 'speakers/speaker_list.html', context)

def speaker_detail(request, pk):
    """
    Vista para ver los detalles de un ponente.
    """
    speaker = get_object_or_404(SpeakerProfile, pk=pk)
    presentations = speaker.presentations.all().order_by('-date')
    
    # Obtener sesiones futuras donde el ponente participará
    upcoming_sessions = Session.objects.filter(
        speakers=speaker.user,
        start_time__gt=timezone.now()
    ).order_by('start_time')
    
    # Obtener sesiones pasadas donde el ponente participó
    past_sessions = Session.objects.filter(
        speakers=speaker.user,
        start_time__lte=timezone.now()
    ).order_by('-start_time')
    
    context = {
        'speaker': speaker,
        'presentations': presentations,
        'upcoming_sessions': upcoming_sessions,
        'past_sessions': past_sessions
    }
    
    return render(request, 'speakers/speaker_detail.html', context)

@login_required
def speaker_profile_create(request):
    """
    Vista para crear un perfil de ponente.
    """
    # Verificar si el usuario ya tiene un perfil de ponente
    try:
        speaker = SpeakerProfile.objects.get(user=request.user)
        messages.info(request, _('You already have a speaker profile.'))
        return redirect('speaker_profile_update')
    except SpeakerProfile.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = SpeakerProfileForm(request.POST)
        if form.is_valid():
            speaker_profile = form.save(commit=False)
            speaker_profile.user = request.user
            speaker_profile.save()
            form.save_m2m()  # Guardar relaciones many-to-many
            
            messages.success(request, _('Your speaker profile has been created!'))
            return redirect('speaker_detail', pk=speaker_profile.pk)
    else:
        form = SpeakerProfileForm()
    
    context = {
        'form': form,
        'title': _('Create Speaker Profile')
    }
    
    return render(request, 'speakers/speaker_form.html', context)

@login_required
def speaker_profile_update(request):
    """
    Vista para actualizar el perfil de ponente.
    """
    speaker = get_object_or_404(SpeakerProfile, user=request.user)
    
    if request.method == 'POST':
        form = SpeakerProfileForm(request.POST, instance=speaker)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your speaker profile has been updated!'))
            return redirect('speaker_detail', pk=speaker.pk)
    else:
        form = SpeakerProfileForm(instance=speaker)
    
    context = {
        'form': form,
        'title': _('Update Speaker Profile')
    }
    
    return render(request, 'speakers/speaker_form.html', context)

@login_required
def presentation_create(request):
    """
    Vista para agregar una presentación.
    """
    speaker = get_object_or_404(SpeakerProfile, user=request.user)
    
    if request.method == 'POST':
        form = PresentationForm(request.POST)
        if form.is_valid():
            presentation = form.save(commit=False)
            presentation.speaker = speaker
            presentation.save()
            
            messages.success(request, _('Your presentation has been added!'))
            return redirect('speaker_detail', pk=speaker.pk)
    else:
        form = PresentationForm()
    
    context = {
        'form': form,
        'title': _('Add Presentation')
    }
    
    return render(request, 'speakers/presentation_form.html', context)

@login_required
def presentation_update(request, pk):
    """
    Vista para actualizar una presentación.
    """
    presentation = get_object_or_404(Presentation, pk=pk)
    
    # Verificar que el usuario sea el dueño de la presentación
    if presentation.speaker.user != request.user:
        messages.error(request, _('You do not have permission to edit this presentation.'))
        return redirect('speaker_detail', pk=presentation.speaker.pk)
    
    if request.method == 'POST':
        form = PresentationForm(request.POST, instance=presentation)
        if form.is_valid():
            form.save()
            messages.success(request, _('Your presentation has been updated!'))
            return redirect('speaker_detail', pk=presentation.speaker.pk)
    else:
        form = PresentationForm(instance=presentation)
    
    context = {
        'form': form,
        'title': _('Update Presentation')
    }
    
    return render(request, 'speakers/presentation_form.html', context)

@login_required
def presentation_delete(request, pk):
    """
    Vista para eliminar una presentación.
    """
    presentation = get_object_or_404(Presentation, pk=pk)
    
    # Verificar que el usuario sea el dueño de la presentación
    if presentation.speaker.user != request.user:
        messages.error(request, _('You do not have permission to delete this presentation.'))
        return redirect('speaker_detail', pk=presentation.speaker.pk)
    
    if request.method == 'POST':
        speaker_pk = presentation.speaker.pk
        presentation.delete()
        messages.success(request, _('Your presentation has been deleted!'))
        return redirect('speaker_detail', pk=speaker_pk)
    
    context = {
        'presentation': presentation,
    }
    
    return render(request, 'speakers/presentation_delete.html', context)

def specialization_detail(request, slug):
    """
    Vista para ver todos los ponentes de una especialización.
    """
    specialization = get_object_or_404(Specialization, slug=slug)
    speakers = specialization.speakers.all().order_by('-featured', 'user__last_name', 'user__first_name')
    
    # Paginar los resultados
    paginator = Paginator(speakers, 12)  # 12 ponentes por página
    page = request.GET.get('page')
    
    try:
        speakers = paginator.page(page)
    except PageNotAnInteger:
        speakers = paginator.page(1)
    except EmptyPage:
        speakers = paginator.page(paginator.num_pages)
    
    context = {
        'specialization': specialization,
        'speakers': speakers
    }
    
    return render(request, 'speakers/specialization_detail.html', context)