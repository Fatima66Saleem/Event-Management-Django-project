from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test  # ADD THIS IMPORT
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.models import User
from django.utils import timezone

from .models import (
    UserProfile, Department, Event, 
    EventRegistration, EventReview, Notification
)
from .forms import (
    UserRegistrationForm, EventForm, 
    EventRegistrationForm, EventReviewForm,
    UserUpdateForm, ProfileUpdateForm
)

# ================ HELPER FUNCTIONS ================
def is_admin(user):
    return user.is_authenticated and (user.is_superuser or 
           (hasattr(user, 'profile') and user.profile.user_type == 'admin'))

def is_faculty(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type in ['faculty', 'admin']

def is_student(user):
    return user.is_authenticated and hasattr(user, 'profile') and user.profile.user_type == 'student'

# ================ AUTHENTICATION VIEWS ================
def home(request):
    """Home page"""
    events = Event.objects.filter(is_active=True).order_by('date')[:6]
    departments = Department.objects.all()[:5]
    
    context = {
        'events': events,
        'departments': departments,
    }
    return render(request, 'home.html', context)

def register_view(request):
    """User registration"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            # Show form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    """User login"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'registration/login.html')

def logout_view(request):
    """User logout"""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

# ================ DASHBOARD VIEWS ================
@login_required
def dashboard(request):
    """Main dashboard"""
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        # Create profile if doesn't exist
        department = Department.objects.first()
        profile = UserProfile.objects.create(
            user=request.user,
            user_type='student',
            department=department
        )
    
    if profile.user_type == 'student':
        return student_dashboard(request)
    elif profile.user_type in ['faculty', 'admin']:
        return faculty_dashboard(request)
    else:
        # Default to student dashboard
        return student_dashboard(request)

@login_required
def student_dashboard(request):
    """Student dashboard"""
    registrations = EventRegistration.objects.filter(
        student=request.user
    ).select_related('event').order_by('-registration_date')
    
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context = {
        'registrations': registrations,
        'notifications': notifications,
    }
    return render(request, 'dashboard/student.html', context)

@login_required
def faculty_dashboard(request):
    """Faculty dashboard"""
    created_events = Event.objects.filter(
        created_by=request.user
    ).order_by('-created_at')
    
    # Get user's department events
    department_events = []
    if hasattr(request.user, 'profile') and request.user.profile.department:
        department_events = Event.objects.filter(
            department=request.user.profile.department
        ).exclude(created_by=request.user).order_by('-created_at')[:10]
    
    notifications = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).order_by('-created_at')[:5]
    
    context = {
        'created_events': created_events,
        'department_events': department_events,
        'notifications': notifications,
    }
    return render(request, 'dashboard/faculty.html', context)

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard"""
    total_users = User.objects.count()
    total_events = Event.objects.count()
    total_departments = Department.objects.count()
    
    pending_faculty = UserProfile.objects.filter(
        user_type='faculty',
        is_approved=False
    ).count()
    
    context = {
        'total_users': total_users,
        'total_events': total_events,
        'total_departments': total_departments,
        'pending_faculty': pending_faculty,
    }
    return render(request, 'dashboard/admin.html', context)

# ================ PROFILE VIEWS ================
@login_required
def profile_view(request):
    """User profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(
            request.POST, 
            request.FILES, 
            instance=request.user.profile
        )
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    
    return render(request, 'registration/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

# ================ EVENT VIEWS ================
def all_events(request):
    """All events page"""
    events = Event.objects.filter(is_active=True).order_by('date', 'time')
    
    # Filtering
    department_id = request.GET.get('department')
    event_type = request.GET.get('event_type')
    search = request.GET.get('search')
    
    if department_id:
        events = events.filter(department_id=department_id)
    
    if event_type:
        events = events.filter(event_type=event_type)
    
    if search:
        events = events.filter(
            Q(title__icontains=search) | 
            Q(description__icontains=search) |
            Q(location__icontains=search)
        )
    
    departments = Department.objects.all()
    
    return render(request, 'events/all_events.html', {
        'events': events,
        'departments': departments,
        'event_types': Event.EVENT_TYPES,
    })

def event_detail(request, event_id):
    """Event detail page"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user is registered
    is_registered = False
    registration = None
    if request.user.is_authenticated:
        registration = EventRegistration.objects.filter(
            event=event,
            student=request.user
        ).first()
        is_registered = registration is not None
    
    # Get reviews
    reviews = EventReview.objects.filter(event=event).order_by('-created_at')
    
    # Review form
    review_form = EventReviewForm()
    
    context = {
        'event': event,
        'is_registered': is_registered,
        'registration': registration,
        'reviews': reviews,
        'review_form': review_form,
        'available_seats': event.get_available_seats(),
    }
    return render(request, 'events/event_detail.html', context)

@login_required
@user_passes_test(is_faculty)
def create_event(request):
    """Create new event"""
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.save()
            messages.success(request, 'Event created successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm()
        # Set default department to user's department
        if hasattr(request.user, 'profile') and request.user.profile.department:
            form.fields['department'].initial = request.user.profile.department
    
    return render(request, 'events/create_event.html', {'form': form})

@login_required
@user_passes_test(is_faculty)
def update_event(request, event_id):
    """Update event"""
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            messages.success(request, 'Event updated successfully!')
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/update_event.html', {'form': form, 'event': event})

@login_required
@user_passes_test(is_faculty)
def delete_event(request, event_id):
    """Delete event"""
    event = get_object_or_404(Event, id=event_id, created_by=request.user)
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Event deleted successfully!')
        return redirect('dashboard')
    
    return render(request, 'events/delete_event.html', {'event': event})

# ================ REGISTRATION VIEWS ================
@login_required
def register_for_event(request, event_id):
    """Register for event"""
    # Check if user is student
    if not hasattr(request.user, 'profile') or request.user.profile.user_type != 'student':
        messages.error(request, 'Only students can register for events!')
        return redirect('event_detail', event_id=event_id)
    
    event = get_object_or_404(Event, id=event_id)
    
    # Check if already registered
    if EventRegistration.objects.filter(event=event, student=request.user).exists():
        messages.warning(request, 'You are already registered for this event!')
        return redirect('event_detail', event_id=event_id)
    
    # Check available seats
    if event.get_available_seats() <= 0:
        messages.error(request, 'No seats available for this event!')
        return redirect('event_detail', event_id=event_id)
    
    # Check if registration is open
    if not event.is_registration_open():
        messages.error(request, 'Registration is closed for this event!')
        return redirect('event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = EventRegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
            registration.event = event
            registration.student = request.user
            registration.save()
            
            # Create notification for event creator
            if event.created_by:
                Notification.objects.create(
                    user=event.created_by,
                    title='New Registration',
                    message=f'{request.user.get_full_name()} registered for your event "{event.title}"',
                )
            
            messages.success(request, 'Successfully registered for the event!')
            return redirect('event_detail', event_id=event_id)
    else:
        form = EventRegistrationForm()
    
    return render(request, 'events/register_event.html', {
        'event': event,
        'form': form
    })

@login_required
def cancel_registration(request, registration_id):
    """Cancel registration"""
    registration = get_object_or_404(
        EventRegistration, 
        id=registration_id, 
        student=request.user
    )
    
    if request.method == 'POST':
        registration.status = 'cancelled'
        registration.save()
        messages.success(request, 'Registration cancelled successfully!')
    
    return redirect('dashboard')

@login_required
def submit_review(request, event_id):
    """Submit event review"""
    event = get_object_or_404(Event, id=event_id)
    
    # Check if user attended the event
    attended = EventRegistration.objects.filter(
        event=event,
        student=request.user,
        status='attended'
    ).exists()
    
    if not attended:
        messages.error(request, 'You must attend the event to submit a review')
        return redirect('event_detail', event_id=event_id)
    
    if request.method == 'POST':
        form = EventReviewForm(request.POST)
        if form.is_valid():
            # Check if already reviewed
            existing_review = EventReview.objects.filter(
                event=event,
                user=request.user
            ).first()
            
            if existing_review:
                messages.warning(request, 'You have already reviewed this event!')
                return redirect('event_detail', event_id=event_id)
            
            review = form.save(commit=False)
            review.event = event
            review.user = request.user
            review.save()
            messages.success(request, 'Thank you for your review!')
    
    return redirect('event_detail', event_id=event_id)

# ================ ADMIN VIEWS ================
@login_required
@user_passes_test(is_admin)
def manage_faculty(request):
    """Manage faculty approvals"""
    pending_faculty = UserProfile.objects.filter(
        user_type='faculty',
        is_approved=False
    )
    
    approved_faculty = UserProfile.objects.filter(
        user_type='faculty',
        is_approved=True
    )
    
    if request.method == 'POST':
        profile_id = request.POST.get('profile_id')
        action = request.POST.get('action')
        
        profile = get_object_or_404(UserProfile, id=profile_id)
        
        if action == 'approve':
            profile.is_approved = True
            profile.save()
            messages.success(request, f'Approved {profile.user.get_full_name()}')
        elif action == 'reject':
            profile.delete()
            messages.success(request, 'Faculty application rejected')
    
    return render(request, 'admin/manage_faculty.html', {
        'pending_faculty': pending_faculty,
        'approved_faculty': approved_faculty,
    })

# ================ OTHER VIEWS ================
def about(request):
    """About page"""
    return render(request, 'pages/about.html')

def contact(request):
    """Contact page"""
    if request.method == 'POST':
        # Handle contact form
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would typically send an email
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('contact')
    
    return render(request, 'pages/contact.html')

@login_required
def calendar_view(request):
    events = Event.objects.all().values('id', 'title', 'date', 'time', 'location', 'event_type', 'description')
    event_list = list(events)
    return render(request, 'events/calendar.html', {'events_json': event_list})