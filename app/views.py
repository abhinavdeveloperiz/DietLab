# import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import Appoinment_Form,ContactUs_Form
from .models import Appointment, AppointmentPrice,ContactUs,Insurance
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail,send_mass_mail
from django.contrib import messages


from django.core.mail import send_mass_mail

# def send_payment_success_email(appointment):
#     subject_customer = "Your Appointment Payment Was Successful"
#     message_customer = (
#     f"Dear {appointment.name},\n\n"
#     f"We are pleased to inform you that your payment has been successfully received.\n\n"
#     f"📄 **Appointment Confirmation**\n"
#     f"-----------------------------------\n"
#     f"• **Appointment ID:** #{appointment.id}\n"
#     f"• **Date:** {appointment.slot.date}\n"
#     f"• **Time:** {appointment.time}\n"
#     f"-----------------------------------\n\n"
#     f"Thank you for choosing **DietLab** for your health and wellness journey.\n"
#     f"If you have any questions or need assistance, feel free to contact us.\n\n"
#     f"Best regards,\n"
#     f"**The DietLab Team**"
# )


#     subject_admin = "New Appointment"
#     message_admin = (
#         f"• New appointment booked by {appointment.name}.\n\n"
#         f"• Appointment ID: #{appointment.id}\n"
#         f"• Email: {appointment.email}\n"
#         f"• Phone: {appointment.phone}\n"
#         f"• Time:{appointment.time}\n"
#         f"• Booked Date: {appointment.slot.date}\n"
#         f"• Allergy: {appointment.have_any_allergy}\n"
#         f"• Allergy Details: {appointment.allergy_details}\n\n"
#         "Please check the dashboard for more details."
#     )

#     messages = [
#         (subject_customer, message_customer, 'priya05uk@gmail.com', [appointment.email]),
#         (subject_admin, message_admin, 'priya05uk@gmail.com', ['priya05uk@gmail.com']),
#     ]

#     send_mass_mail(messages, fail_silently=False)
    

    
def Home_view(request):
    insurance=Insurance.objects.all()
    return render(request,"home.html",{"insurance":insurance})

def Aboutus_view(request):
    return render(request,"about.html")

def Service_view(request):
    return render(request,"service.html")


def Gallery_view(request):
    return render(request,'gallery.html')



# stripe.api_key = settings.STRIPE_SECRET_KEY 

# def Appoinment_view(request):
#     if not request.session.session_key:
#         request.session.create()  # 🔐 Ensure session is created
    
#     prices = AppointmentPrice.objects.all()
#     if request.method == "POST":
#         form = Appoinment_Form(request.POST)
#         if form.is_valid():
#             appointment = form.save(commit=False)
#             appointment.is_paid = False
#             appointment.session_key = request.session.session_key

#             selected_price_obj = form.cleaned_data['price'] 

#             price_in_pence = int(selected_price_obj.price * 100)
            
#             appointment.save()

#             checkout_session = stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=[{
#                     'price_data': {
#                         'currency': 'gbp',
#                         'unit_amount': price_in_pence,
#                         'product_data': {
#                             'name': 'Dietition Appointment Booking',
#                         },
#                     },
#                     'quantity': 1,
#                 }],
#                 mode='payment',
#                 success_url=request.build_absolute_uri('/payment-success/') + f'?appointment_id={appointment.id}',
#                 cancel_url=request.build_absolute_uri('/payment-cancelled/'),
#             )

#             return redirect(checkout_session.url, code=303)
#     else:
#         form = Appoinment_Form()

#     return render(request, "appoinment.html", {"form": form,"price_list": prices})



# def My_Appointments_view(request):

#     session_key = request.session.session_key
#     appointments = Appointment.objects.filter(session_key=session_key).order_by('-booked_on')

#     return render(request, 'my_appointments.html', {'appointments': appointments})




# def payment_cancelled(request):
#     return render(request, "payment_cancelled.html")



# def payment_success(request):
#     appointment_id = request.GET.get('appointment_id')
#     appointment = get_object_or_404(Appointment, id=appointment_id)
#     appointment.is_paid = True
#     appointment.save()

#     # Send confirmation email to the customer
#     send_payment_success_email(appointment)

#     return render(request, "payment_success.html", {"appointment": appointment})



from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages

def ContactUs_view(request):
    if request.method == "POST":
        form = ContactUs_Form(request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data.get('time')
            
            # Double-check if time slot is still available
            if not time_slot.is_available:
                messages.error(request, "Sorry, this time slot has just been booked. Please choose another time.")
                return render(request, "contact.html", {"form": form})
            
            try:
                # Save the form instance
                instance = form.save()

                # Prepare email content
                customer_subject = "Your DietLab Consultation Has Been Successfully Booked!"
                customer_text_content = f"""
Dear {instance.name},

Your consultation booking has been confirmed with the following details:

Full Name: {instance.name}
Age: {instance.age}
Email: {instance.email}
Phone: {instance.phone}
Health Goals: {instance.goal}
Medical History: {instance.any_medical_history}
Medical Details: {instance.medical_history_details or 'None provided'}
Selected Date: {instance.time.date}
Selected Time: {instance.time}

We look forward to meeting you!

Best regards,
DietLab Team
"""
                customer_html_content = f"""
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Consultation Booking Confirmation</title>
    </head>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6fa; color: #333;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="background-color: #0D47A1; color: white; padding: 30px; text-align: center;">
                <h2 style="margin: 0;">🎉 Booking Confirmed!</h2>
                <p style="margin-top: 8px;">Thanks for booking your consultation with DietLab</p>
            </div>
            <div style="padding: 30px;">
                <p>👋 Hello <strong>{instance.name}</strong>,</p>
                <p>Your consultation has been successfully booked. Here are your details:</p>
                <p>🧑 <strong>Name:</strong> {instance.name}</p>
                <p>🎂 <strong>Age:</strong> {instance.age}</p>
                <p>📧 <strong>Email:</strong> {instance.email}</p>
                <p>📞 <strong>Phone:</strong> <a href="tel:{instance.phone}" style="color: #0D47A1;">{instance.phone}</a></p>
                <p>🎯 <strong>Health Goals:</strong> {instance.goal}</p>
                <p>⚠️ <strong>Medical History:</strong> {instance.any_medical_history}</p>
                <p>📝 <strong>Medical Details:</strong> {instance.medical_history_details or 'None provided'}</p>
                <p>📅 <strong>Date:</strong> {instance.time.date}</p>
                <p>🕒 <strong>Time:</strong> {instance.time}</p>
                <p style="margin-top: 20px; color: #666;">We look forward to helping you achieve your health goals!</p>
            </div>
        </div>
    </body>
</html>
"""
                # Prepare owner notification email
                owner_subject = f"New Consultation Booking - {instance.name}"
                owner_text_content = f"""
New consultation booking received:

Full Name: {instance.name}
Age: {instance.age}
Email: {instance.email}
Phone: {instance.phone}
Health Goals: {instance.goal}
Medical History: {instance.any_medical_history}
Medical Details: {instance.medical_history_details or 'None provided'}
Selected Date: {instance.time.date}
Selected Time: {instance.time}
"""
                owner_html_content = f"""
<html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>New Consultation Booking</title>
    </head>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f6fa; color: #333;">
        <div style="max-width: 600px; margin: 20px auto; background-color: #ffffff; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.1);">
            <div style="background-color: #0D47A1; color: white; padding: 30px; text-align: center;">
                <h2 style="margin: 0;">📬 New Booking Received</h2>
                <p style="margin-top: 8px;">Consultation scheduled by {instance.name}</p>
            </div>
            <div style="padding: 30px;">
                <p>🧑 <strong>Name:</strong> {instance.name}</p>
                <p>🎂 <strong>Age:</strong> {instance.age}</p>
                <p>📧 <strong>Email:</strong> {instance.email}</p>
                <p>📞 <strong>Phone:</strong> {instance.phone}</p>
                <p>🎯 <strong>Health Goals:</strong> {instance.goal}</p>
                <p>⚠️ <strong>Medical History:</strong> {instance.any_medical_history}</p>
                <p>📝 <strong>Medical Details:</strong> {instance.medical_history_details or 'None provided'}</p>
                <p>📅 <strong>Date:</strong> {instance.time.date}</p>
                <p>🕒 <strong>Time:</strong> {instance.time}</p>
            </div>
        </div>
    </body>
</html>
"""
                try:
                    # Send customer confirmation email
                    customer_email = EmailMultiAlternatives(
                        customer_subject,
                        customer_text_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [instance.email]
                    )
                    customer_email.attach_alternative(customer_html_content, "text/html")
                    customer_email.send()

                    # Send owner notification email
                    owner_email = EmailMultiAlternatives(
                        owner_subject,
                        owner_text_content,
                        settings.DEFAULT_FROM_EMAIL,
                        [settings.CONTACT_EMAIL]
                    )
                    owner_email.attach_alternative(owner_html_content, "text/html")
                    owner_email.send()

                    messages.success(request, "Your consultation has been booked successfully! Check your email for confirmation.")
                    return redirect('contact')

                except Exception as e:
                    print(f"Error sending email: {str(e)}")
                    messages.warning(request, "Booking saved but there was an issue sending confirmation emails.")
                    return redirect('contact')

            except Exception as e:
                print(f"Error saving booking: {str(e)}")
                messages.error(request, "An error occurred while processing your booking. Please try again.")
                return render(request, "contact.html", {"form": form})

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ContactUs_Form()

    return render(request, "contact.html", {"form": form})


