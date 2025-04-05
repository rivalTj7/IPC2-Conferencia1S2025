from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from apps.users.models import CustomUser

class Specialization(models.Model):
    """
    Modelo para especializaciones de ponentes.
    """
    name = models.CharField(_('name'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    description = models.TextField(_('description'), blank=True)
    
    class Meta:
        verbose_name = _('specialization')
        verbose_name_plural = _('specializations')
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('specialization_detail', kwargs={'slug': self.slug})

class SpeakerProfile(models.Model):
    """
    Modelo para perfiles de ponentes.
    Extiende la información del CustomUser.
    """
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
        related_name='speaker_profile',
        verbose_name=_('user')
    )
    specializations = models.ManyToManyField(
        Specialization,
        related_name='speakers',
        verbose_name=_('specializations'),
        blank=True
    )
    headline = models.CharField(_('headline'), max_length=200, blank=True)
    bio_extended = models.TextField(_('extended biography'), blank=True)
    website = models.URLField(_('website'), blank=True)
    twitter_handle = models.CharField(_('twitter handle'), max_length=50, blank=True)
    linkedin_url = models.URLField(_('linkedin URL'), blank=True)
    github_username = models.CharField(_('github username'), max_length=50, blank=True)
    featured = models.BooleanField(_('featured'), default=False)
    speaking_experience = models.TextField(_('speaking experience'), blank=True)
    languages = models.CharField(_('languages'), max_length=200, blank=True)
    presentation_topics = models.TextField(_('presentation topics'), blank=True)
    
    class Meta:
        verbose_name = _('speaker profile')
        verbose_name_plural = _('speaker profiles')
        ordering = ['user__last_name', 'user__first_name']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - Speaker Profile"
    
    def get_absolute_url(self):
        return reverse('speaker_detail', kwargs={'pk': self.pk})
    
    def save(self, *args, **kwargs):
        """
        Asegurarse de que el usuario asociado tenga is_speaker=True
        """
        self.user.is_speaker = True
        self.user.save()
        super().save(*args, **kwargs)

class Presentation(models.Model):
    """
    Modelo para presentaciones pasadas dadas por un ponente.
    Útil para mostrar experiencia previa.
    """
    speaker = models.ForeignKey(
        SpeakerProfile,
        on_delete=models.CASCADE,
        related_name='presentations',
        verbose_name=_('speaker')
    )
    title = models.CharField(_('title'), max_length=200)
    event_name = models.CharField(_('event name'), max_length=200)
    date = models.DateField(_('date'))
    description = models.TextField(_('description'), blank=True)
    video_url = models.URLField(_('video URL'), blank=True)
    slides_url = models.URLField(_('slides URL'), blank=True)
    
    class Meta:
        verbose_name = _('presentation')
        verbose_name_plural = _('presentations')
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.title} at {self.event_name} ({self.date.year})"