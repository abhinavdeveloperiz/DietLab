from django import forms
from app.models import Availabledate,AppointmentPrice,ContactUs,AvailableTime
from django.utils import timezone



from phonenumber_field.formfields import PhoneNumberField as FormPhoneNumberField

from phonenumber_field.formfields import PhoneNumberField



class ContactUs_Form(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'phone-input',
        'type': 'tel',
        'placeholder': 'Enter with country code (eg. +44)',
    }))
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

   
        # Load available times
        available_times = AvailableTime.objects.filter(is_available=True)
        choices = [(None, "Choose an Available Time")]
        for time in available_times:
            time_display = f"{time.start_time.strftime('%I:%M %p')} - {time.end_time.strftime('%I:%M %p')}"
            self.fields['time'].widget.attrs[f'data-date-{time.id}'] = time.date.date.strftime('%Y-%m-%d')
            self.fields['time'].widget.attrs[f'data-time-{time.id}'] = time_display
            choices.append((time.id, time_display))
        self.fields['time'].choices = choices

        
        