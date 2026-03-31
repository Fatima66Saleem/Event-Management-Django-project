from django.db import models
from django.contrib.auth.models import User
import uuid

# 1. Department Model
class Department(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=10, unique=True)
    
    def __str__(self):
        return f"{self.code} - {self.name}"
    
    class Meta:
        ordering = ['name']

# 2. UserProfile Model
class UserProfile(models.Model):
    USER_TYPES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
        ('admin', 'Admin'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='student')
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    roll_number = models.CharField(max_length=50, blank=True, null=True)
    employee_id = models.CharField(max_length=50, blank=True, null=True)
    designation = models.CharField(max_length=100, blank=True, null=True)
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"

# 3. Event Model
class Event(models.Model):
    EVENT_TYPES = [
        ('workshop', 'Workshop'),
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('competition', 'Competition'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES, default='seminar')
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    venue_details = models.TextField(blank=True, null=True)
    max_participants = models.PositiveIntegerField(default=50)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    featured_image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['date', 'time']
    
    def get_registered_count(self):
        return self.registrations.filter(status='confirmed').count()
    
    def get_available_seats(self):
        return self.max_participants - self.get_registered_count()
    
    def is_registration_open(self):
        from django.utils import timezone
        return self.is_active and self.date >= timezone.now().date()

# 4. Event Registration Model
class EventRegistration(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
    ]
    
    registration_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='registrations')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='registrations')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='confirmed')
    additional_notes = models.TextField(blank=True, null=True)
    check_in_time = models.DateTimeField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.student.username} - {self.event.title}"
    
    class Meta:
        unique_together = ['student', 'event']
        ordering = ['-registration_date']

# 5. Event Review Model
class EventReview(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['event', 'user']
    
    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}/5"

# 6. Notification Model
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']