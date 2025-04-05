from django.db import models
from django.utils.translation import gettext_lazy as _

class ContactMessage(models.Model):
    """
    Modelo para mensajes de contacto del formulario de contacto.
    """
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email'))
    subject = models.CharField(_('subject'), max_length=200)
    message = models.TextField(_('message'))
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    read = models.BooleanField(_('read'), default=False)
    
    class Meta:
        verbose_name = _('contact message')
        verbose_name_plural = _('contact messages')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"

class FAQ(models.Model):
    """
    Modelo para preguntas frecuentes.
    """
    question = models.CharField(_('question'), max_length=255)
    answer = models.TextField(_('answer'))
    order = models.PositiveIntegerField(_('order'), default=0)
    
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['order']
    
    def __str__(self):
        return self.question

class Sponsor(models.Model):
    """
    Modelo para patrocinadores.
    """
    class SponsorLevel(models.TextChoices):
        PLATINUM = 'platinum', _('Platinum')
        GOLD = 'gold', _('Gold')
        SILVER = 'silver', _('Silver')
        BRONZE = 'bronze', _('Bronze')
    
    name = models.CharField(_('name'), max_length=100)
    logo = models.ImageField(_('logo'), upload_to='sponsor_logos/')
    website = models.URLField(_('website'), blank=True)
    description = models.TextField(_('description'), blank=True)
    level = models.CharField(
        _('level'),
        max_length=20,
        choices=SponsorLevel.choices,
        default=SponsorLevel.BRONZE
    )
    active = models.BooleanField(_('active'), default=True)
    
    class Meta:
        verbose_name = _('sponsor')
        verbose_name_plural = _('sponsors')
        ordering = ['level', 'name']
    
    def __str__(self):
        return self.name