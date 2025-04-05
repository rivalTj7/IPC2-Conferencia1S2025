from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado que extiende el modelo base de Django.
    Permite agregar campos adicionales al usuario estándar.
    """
    email = models.EmailField(_('email address'), unique=True)
    bio = models.TextField(_('biography'), blank=True)
    profile_picture = models.ImageField(
        _('profile picture'), 
        upload_to='profile_pics/', 
        blank=True,
        null=True
    )
    phone_number = models.CharField(_('phone number'), max_length=15, blank=True)
    organization = models.CharField(_('organization'), max_length=100, blank=True)
    job_title = models.CharField(_('job title'), max_length=100, blank=True)
    is_speaker = models.BooleanField(_('speaker status'), default=False)
    date_modified = models.DateTimeField(_('date modified'), auto_now=True)

    # Campos para configuración de notificaciones
    receive_email_notifications = models.BooleanField(
        _('receive email notifications'), 
        default=True
    )
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.get_full_name() or self.username