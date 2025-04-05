from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from apps.users.models import CustomUser

class Category(models.Model):
    """
    Modelo para categorías de eventos.
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Location(models.Model):
    """
    Modelo para ubicaciones de eventos.
    """
    name = models.CharField(_('name'), max_length=100)
    address = models.CharField(_('address'), max_length=255)
    city = models.CharField(_('city'), max_length=100)
    state = models.CharField(_('state'), max_length=100)
    country = models.CharField(_('country'), max_length=100)
    capacity = models.PositiveIntegerField(_('capacity'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name}, {self.city}"

class Event(models.Model):
    """
    Modelo para eventos.
    """
    class EventStatus(models.TextChoices):
        DRAFT = 'draft', _('Draft')
        PUBLISHED = 'published', _('Published')
        CANCELLED = 'cancelled', _('Cancelled')
        COMPLETED = 'completed', _('Completed')
    
    title = models.CharField(_('title'), max_length=200)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'))
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        related_name='events',
        null=True,
        blank=True,
        verbose_name=_('category')
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='events',
        null=True,
        blank=True,
        verbose_name=_('location')
    )
    start_date = models.DateTimeField(_('start date'))
    end_date = models.DateTimeField(_('end date'))
    image = models.ImageField(_('image'), upload_to='event_images/', blank=True, null=True)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=EventStatus.choices,
        default=EventStatus.DRAFT
    )
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    registration_required = models.BooleanField(_('registration required'), default=True)
    max_attendees = models.PositiveIntegerField(_('maximum attendees'), blank=True, null=True)
    organizer = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='organized_events',
        verbose_name=_('organizer')
    )
    attendees = models.ManyToManyField(
        CustomUser,
        through='Registration',
        related_name='attended_events',
        verbose_name=_('attendees')
    )
    is_featured = models.BooleanField(_('featured'), default=False)
    
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-start_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('event_detail', kwargs={'slug': self.slug})
    
    @property
    def is_past(self):
        from django.utils import timezone
        return self.end_date < timezone.now()
    
    @property
    def registered_count(self):
        return self.registrations.count()
    
    @property
    def available_spots(self):
        if not self.max_attendees:
            return None  # Unlimited
        return max(0, self.max_attendees - self.registered_count)

class Session(models.Model):
    """
    Modelo para sesiones dentro de un evento.
    """
    title = models.CharField(_('title'), max_length=200)
    description = models.TextField(_('description'))
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='sessions',
        verbose_name=_('event')
    )
    start_time = models.DateTimeField(_('start time'))
    end_time = models.DateTimeField(_('end time'))
    room = models.CharField(_('room'), max_length=100, blank=True)
    speakers = models.ManyToManyField(
        CustomUser,
        limit_choices_to={'is_speaker': True},
        related_name='speaking_sessions',
        verbose_name=_('speakers')
    )
    
    class Meta:
        verbose_name = _('session')
        verbose_name_plural = _('sessions')
        ordering = ['start_time']
    
    def __str__(self):
        return f"{self.title} ({self.event.title})"

class Registration(models.Model):
    """
    Modelo para registros de asistentes a eventos.
    """
    class RegistrationStatus(models.TextChoices):
        PENDING = 'pending', _('Pending')
        CONFIRMED = 'confirmed', _('Confirmed')
        CANCELLED = 'cancelled', _('Cancelled')
        ATTENDED = 'attended', _('Attended')
    
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_('user')
    )
    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE,
        related_name='registrations',
        verbose_name=_('event')
    )
    registration_date = models.DateTimeField(_('registration date'), auto_now_add=True)
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=RegistrationStatus.choices,
        default=RegistrationStatus.PENDING
    )
    notes = models.TextField(_('notes'), blank=True)
    
    class Meta:
        verbose_name = _('registration')
        verbose_name_plural = _('registrations')
        unique_together = ['user', 'event']
        ordering = ['-registration_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"