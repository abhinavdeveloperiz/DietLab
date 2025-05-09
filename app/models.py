from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from datetime import time



class AppointmentPrice(models.Model):
    price_choices=[
        ("1 Day","1 Day"),
        ("3 Month","3 Month"),
        ("6 Month","6 Month"),
    ]
    # currency_choices = [
    #     ("gbp", "GBP (£)"),
    #     ("inr", "INR (₹)"),
    #     ("aed", "AED (د.إ)"),
    #     ("sar", "SAR (ر.س)"),
    # ]
    price_choise=models.CharField(max_length=100,choices=price_choices,default="1 Day")
    price = models.DecimalField(max_digits=6, decimal_places=0) 
    # currency = models.CharField(max_length=10, choices=currency_choices, default="gbp")  
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.price_choise} - £{self.price}"
    
class Availabledate(models.Model):
    date = models.DateField(unique=True)

    def __str__(self):
        return self.date.strftime('%Y-%m-%d') 
    
    def create_time_slot(self):
        """"Create time slots for this date."""

        time_slot=[
            (time(10, 0), time(10, 30)),
            (time(10, 30), time(11, 0)),
            (time(11,0),time(11,30)),
            (time(11,30),time(12,0)),
            (time(12, 0), time(12, 30)),
            (time(12, 30), time(13, 0)),
            (time(13, 0), time(13, 30)),
            (time(13, 30), time(14, 0)),
            (time(14, 0), time(14, 30)),
            
        ]
        for start_time,end_time in time_slot:
            AvailableTime.objects.create(
                date=self,
                start_time=start_time,
                end_time=end_time,
                is_available=True
            )
    
from django.db import models
from django.core.exceptions import ValidationError

class AvailableTime(models.Model):
    date = models.ForeignKey(Availabledate, on_delete=models.CASCADE)
    start_time = models.TimeField(help_text="Enter time in UK timezone")
    end_time = models.TimeField(help_text="Enter time in UK timezone")
    is_available = models.BooleanField(default=True)
    timezone = models.CharField(max_length=50, default='Europe/London')

    class Meta:
        unique_together = ('date', 'start_time', 'end_time')
        ordering = ['date', 'start_time']

    def __str__(self):
        return f"{self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')} (UK)"

    

class Appointment(models.Model):

    name = models.CharField(max_length=100)
    age = models.IntegerField()
    email = models.EmailField()
    phone = PhoneNumberField(region=None)
    goal = models.TextField()
    choices=(
        ("YES","YES"),
        ("NO","NO"),
    )
    
    time = models.CharField(max_length=100)
    have_any_allergy = models.CharField(choices=choices,default="NO")
    allergy_details = models.CharField(max_length=255, blank=True, null=True)
    slot = models.ForeignKey(Availabledate, on_delete=models.CASCADE)
    booked_on = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)
    price= models.ForeignKey(AppointmentPrice,on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)


    def __str__(self):
        return f"{self.name} - {self.slot.date}"
    

    


from django.utils import timezone

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField()
    email = models.EmailField()
    phone = PhoneNumberField()    
    goal = models.TextField()
    choices = (
        ("YES", "YES"),
        ("NO", "NO"),
    )
    any_medical_history = models.CharField(choices=choices, default="NO")
    medical_history_details = models.CharField(max_length=255, blank=True, null=True)
    time = models.ForeignKey(AvailableTime,on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.name} - {self.time}"
    
    def save(self,*args,**kwargs):
        self.time.is_available=False
        self.time.save()
        super().save(*args,**kwargs)



class Insurance(models.Model):
    image=models.ImageField(upload_to="inspurance")
    name=models.CharField(max_length=200)