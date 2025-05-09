from django import forms
from app.models import Appointment,Availabledate,AppointmentPrice,ContactUs,AvailableTime
from django.utils import timezone


class Appoinment_Form(forms.ModelForm):
    TIME_CHOICES = [
        ('10:00 - 11:00 AM', '10:00 - 11:00 AM'),
        ('11:00 - 12:00 AM', '11:00 - 12:00 AM'),
        
        ('02:00 - 03:00 PM', '02:00 - 03:00 PM'),
        ('04:00 - 05:00 PM', '04:00 - 05:00 PM'),
    ]

    time = forms.ChoiceField(
        choices=TIME_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input border border-black'}),
        label="Select a Time Slot"
    )

    class Meta:
        model = Appointment
        fields = ["name", "age","email", "phone","goal", "have_any_allergy", "allergy_details", "slot", "time","price"]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your name"
            }),
            "age": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your age"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email"
            }),
            "phone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your Number"
            }),
            "goal": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Mention your goal (e.g. weight loss, diabetes management)"
            }),
            "have_any_allergy": forms.Select(attrs={
                "class": "form-select"
            }),
            "allergy_details": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 2,
                "placeholder": "If yes, specify the allergy details"
            }),
            "slot": forms.Select(attrs={"class": "form-control date-select"}),

            "price":forms.Select(attrs={"class":"form-select"}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Show all slots regardless of is_active status
        self.fields['slot'].queryset = Availabledate.objects.all().order_by('date')

from phonenumber_field.formfields import PhoneNumberField as FormPhoneNumberField


class ContactUs_Form(forms.ModelForm):
    phone = FormPhoneNumberField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Number With Country Code',
            'id': 'phone' 
        })
    )
   

    class Meta:
        model = ContactUs
        fields = ['name', 'age', 'email', 'phone', 'goal', 'any_medical_history', 'medical_history_details','time']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your full name'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email address'}),
            'goal': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'What is your fitness goal?', 'rows': 3}),
            'any_medical_history': forms.Select(attrs={'class': 'form-control'}),
            'medical_history_details': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'If Yes, Mention Medical Details', 'rows': 3}),
            'time': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Choose an Available Time'}),            
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get available time slots with date information
        available_times = AvailableTime.objects.filter(
            is_available=True
        ).select_related('date').order_by('date__date', 'start_time')

        # Add data attributes for date and time
        choices = [(None, "Choose an Available Time")]  # Add empty choice
        for time in available_times:
            time_display = f"{time.start_time.strftime('%I:%M %p')} - {time.end_time.strftime('%I:%M %p')}"
            self.fields['time'].widget.attrs[f'data-date-{time.id}'] = time.date.date.strftime('%Y-%m-%d')
            self.fields['time'].widget.attrs[f'data-time-{time.id}'] = time_display
            choices.append((time.id, time_display))
        
        self.fields['time'].choices = choices
        
    def clean_time(self):
        time = self.cleaned_data.get('time')
        if time:
            # Double check availability
            if not AvailableTime.objects.filter(
                id=time.id, 
                is_available=True
            ).exists():
                raise forms.ValidationError("This time slot is no longer available")
        return time
        
        