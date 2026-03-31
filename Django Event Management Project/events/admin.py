from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    UserProfile, Department, Event, 
    EventRegistration, EventReview, Notification
)

# Inline for UserProfile
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

# Register models
@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'date', 'location', 'created_by']
    list_filter = ['event_type', 'date', 'department']
    search_fields = ['title', 'description', 'location']

@admin.register(EventRegistration)
class EventRegistrationAdmin(admin.ModelAdmin):
    list_display = ['student', 'event', 'status', 'registration_date']
    list_filter = ['status', 'registration_date']
    search_fields = ['student__username', 'event__title']

@admin.register(EventReview)
class EventReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['title', 'message']

# Unregister default User admin and register custom
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Admin site customization
admin.site.site_header = "Event Management System Admin"
admin.site.site_title = "Event Management System"
admin.site.index_title = "Dashboard"