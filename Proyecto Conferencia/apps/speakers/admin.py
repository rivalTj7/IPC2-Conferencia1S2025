from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Specialization, SpeakerProfile, Presentation

@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

class PresentationInline(admin.TabularInline):
    model = Presentation
    extra = 1

@admin.register(SpeakerProfile)
class SpeakerProfileAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'headline', 'featured', 'get_specializations')
    list_filter = ('featured', 'specializations')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'headline', 'bio_extended')
    filter_horizontal = ('specializations',)
    inlines = [PresentationInline]
    
    fieldsets = (
        (None, {
            'fields': ('user', 'headline', 'bio_extended', 'featured')
        }),
        (_('Specializations and Topics'), {
            'fields': ('specializations', 'speaking_experience', 'presentation_topics')
        }),
        (_('Social Media and Contact'), {
            'fields': ('website', 'twitter_handle', 'linkedin_url', 'github_username')
        }),
        (_('Additional Information'), {
            'fields': ('languages',)
        }),
    )
    
    def get_full_name(self, obj):
        return obj.user.get_full_name()
    get_full_name.short_description = _('Name')
    
    def get_specializations(self, obj):
        return ", ".join([spec.name for spec in obj.specializations.all()])
    get_specializations.short_description = _('Specializations')

@admin.register(Presentation)
class PresentationAdmin(admin.ModelAdmin):
    list_display = ('title', 'speaker_name', 'event_name', 'date')
    list_filter = ('date',)
    search_fields = ('title', 'event_name', 'description', 'speaker__user__first_name', 'speaker__user__last_name')
    date_hierarchy = 'date'
    
    def speaker_name(self, obj):
        return obj.speaker.user.get_full_name()
    speaker_name.short_description = _('Speaker')