from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    
    # Profile
    path('profile/', views.profile_view, name='profile'),
    
    # Events
    path('events/', views.all_events, name='all_events'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.create_event, name='create_event'),
    path('events/<int:event_id>/edit/', views.update_event, name='update_event'),
    path('events/<int:event_id>/delete/', views.delete_event, name='delete_event'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('events/<int:event_id>/review/', views.submit_review, name='submit_review'),
    path('calendar/', views.calendar_view, name='calendar'),
    
    # Registration Management
    path('registration/<int:registration_id>/cancel/', views.cancel_registration, name='cancel_registration'),
    
    # Admin
    path('admin/faculty/', views.manage_faculty, name='manage_faculty'),
    
    # Pages
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]