from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Event, EventRegistration, EventReview, Department

# User Registration Form
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    USER_TYPE_CHOICES = [
        ('student', 'Student'),
        ('faculty', 'Faculty'),
    ]
    
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    roll_number = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    employee_id = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    designation = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields required except roll_number, employee_id, designation
        for field in self.fields:
            self.fields[field].required = True
        self.fields['roll_number'].required = False
        self.fields['employee_id'].required = False
        self.fields['designation'].required = False
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Create user profile
            profile = UserProfile.objects.create(
                user=user,
                user_type=self.cleaned_data['user_type'],
                phone=self.cleaned_data['phone'],
                department=self.cleaned_data['department'],
            )
            
            if self.cleaned_data['user_type'] == 'student':
                profile.roll_number = self.cleaned_data['roll_number']
            else:
                profile.employee_id = self.cleaned_data['employee_id']
                profile.designation = self.cleaned_data['designation']
            
            profile.save()
        
        return user

# Event Creation Form
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'title', 'description', 'event_type', 'date', 'time', 
            'location', 'venue_details', 'max_participants', 'department',
            'featured_image'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'event_type': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'venue_details': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'max_participants': forms.NumberInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
            'featured_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

# Event Registration Form
class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = ['additional_notes']
        widgets = {
            'additional_notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requirements...'}),
        }

# Event Review Form
class EventReviewForm(forms.ModelForm):
    class Meta:
        model = EventReview
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Share your experience...'}),
        }

# User Profile Update Form
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone', 'profile_picture', 'department']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.FileInput(attrs={'class': 'form-control'}),
            'department': forms.Select(attrs={'class': 'form-control'}),
        }