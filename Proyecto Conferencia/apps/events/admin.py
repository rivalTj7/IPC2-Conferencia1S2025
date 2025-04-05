from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import Category, Location, Event, Session, Registration

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country', 'capacity')
    list_filter = ('country', 'city')
    search_fields = ('name', 'address', 'city')

class SessionInline(admin.TabularInline):
    model = Session
    extra = 1
    filter_horizontal = ('speakers',)

class RegistrationInline(admin.TabularInline):
    model = Registration
    extra = 0
    readonly_fields = ('registration_date',)
    raw_id_fields = ('user',)

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_date', 'end_date', 'location', 'status', 'registered_count')
    list_filter = ('status', 'start_date', 'category', 'is_featured')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'start_date'
    inlines = [SessionInline, RegistrationInline]
    filter_horizontal = ()
    raw_id_fields = ('organizer',)
    
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'image')
        }),
        (_('Category and Location'), {
            'fields': ('category', 'location')
        }),
        (_('Schedule'), {
            'fields': ('start_date', 'end_date')
        }),
        (_('Status and Organization'), {
            'fields': ('status', 'organizer', 'is_featured')
        }),
        (_('Registration'), {
            'fields': ('registration_required', 'max_attendees')
        }),
    )
    
    def registered_count(self, obj):
        return obj.registrations.count()
    registered_count.short_description = _('Registered')

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'event', 'start_time', 'end_time', 'room')
    list_filter = ('event', 'start_time')
    search_fields = ('title', 'description')
    filter_horizontal = ('speakers',)

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'status', 'registration_date')
    list_filter = ('status', 'registration_date', 'event')
    search_fields = ('user__username', 'user__email', 'event__title')
    readonly_fields = ('registration_date',)
    raw_id_fields = ('user', 'event')