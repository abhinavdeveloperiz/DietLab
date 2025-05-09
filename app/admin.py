from django.contrib import admin
from .models import (
    Appointment, 
    Availabledate, 
    AppointmentPrice,
    Insurance,
    AvailableTime,
    ContactUs
)
from django.utils import timezone
from django.contrib import messages

@admin.register(AvailableTime)
class AvailableTimeAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'is_available')
    list_filter = ('date', 'is_available')
    search_fields = ('date__date',)
    list_editable = ('is_available',)
    ordering = ['date', 'start_time']

    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('date', 'start_time', 'end_time')
        return []
  

@admin.register(Availabledate)
class AvailabledateAdmin(admin.ModelAdmin):
    list_display = ('date', 'get_available_slots')
    search_fields = ('date',)
    ordering = ['-date']
    actions = ['create_time_slots']  # Add this line

    def get_available_slots(self, obj):
        available_count = obj.availabletime_set.filter(is_available=True).count()
        total_count = obj.availabletime_set.count()
        return f"{available_count}/{total_count} slots available"
    get_available_slots.short_description = "Available Slots"

    def create_time_slots(self, request, queryset):
        for date in queryset:
            try:
                date.create_time_slot()
                self.message_user(
                    request,
                    f"Successfully created time slots for {date}",
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error creating time slots for {date}: {str(e)}",
                    messages.ERROR
                )
    create_time_slots.short_description = "Create time slots for selected dates"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # Only for new dates
            try:
                obj.create_time_slot()
                self.message_user(
                    request,
                    f"Successfully created time slots for {obj.date}",
                    messages.SUCCESS
                )
            except Exception as e:
                self.message_user(
                    request,
                    f"Error creating time slots: {str(e)}",
                    messages.ERROR
                )

@admin.register(AppointmentPrice)
class AppointmentPriceAdmin(admin.ModelAdmin):
    list_display = ('price_choise', 'price', 'updated_on')
    search_fields = ('price_choise',)
    ordering = ['price']

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'slot', 'time', 'is_paid', 'booked_on')
    list_filter = ('slot__date', 'is_paid', 'have_any_allergy', 'price')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('booked_on', 'session_key')
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'age', 'email', 'phone')
        }),
        ('Health Information', {
            'fields': ('goal', 'have_any_allergy', 'allergy_details')
        }),
        ('Appointment Details', {
            'fields': ('slot', 'time', 'price', 'is_paid')
        }),
        ('System Fields', {
            'fields': ('booked_on', 'session_key'),
            'classes': ('collapse',)
        }),
    )
    def has_add_permission(self, request):
        return False

@admin.register(ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'get_slot_date', 'get_slot_time', 'any_medical_history')
    list_filter = ('time__date', 'any_medical_history')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('time',)

    def get_slot_date(self, obj):
        return obj.time.date.date
    get_slot_date.short_description = 'Date'
    
    def get_slot_time(self, obj):
        return f"{obj.time.start_time.strftime('%I:%M %p')} - {obj.time.end_time.strftime('%I:%M %p')}"
    get_slot_time.short_description = 'Time Slot'

    def has_add_permission(self, request):
        return False

@admin.register(Insurance)
class InsuranceAdmin(admin.ModelAdmin):
    list_display = ('name', 'image')
    search_fields = ('name',)