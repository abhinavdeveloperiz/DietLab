import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import ContactUs_Form
from .models import AppointmentPrice,ContactUs,Insurance,Testimonial
from django.shortcuts import render, get_object_or_404
from django.core.mail import send_mail,send_mass_mail
from django.contrib import messages




    
def Home_view(request):
    insurance=Insurance.objects.all()
    Testimonials=Testimonial.objects.all()
    return render(request,"home.html",{"insurance":insurance,"testimonials":Testimonials})

def Aboutus_view(request):
    return render(request,"about.html")

def Service_view(request):
    return render(request,"service.html")


def Gallery_view(request):
    return render(request,'gallery.html')



from django.contrib import messages


import stripe
from django.conf import settings
from django.shortcuts import redirect

stripe.api_key = settings.STRIPE_SECRET_KEY

def ContactUs_view(request):
    prices = AppointmentPrice.objects.last()
    if request.method == "POST":
        form = ContactUs_Form(request.POST)
        if form.is_valid():
            time_slot = form.cleaned_data.get('time')
            if not time_slot.is_available:
                messages.error(request, "Sorry, this time slot has just been booked. Please choose another time.")
                return render(request, "contact.html", {"form": form})

            instance = form.save(commit=False)
            instance.price = prices
            amount = int(prices.offer_price * 100)  # Stripe expects amount in pence (not paise for GBP)

            instance.save()
            request.session['contact_id'] = instance.id  # store in session for webhook

            # Create Stripe Checkout Session
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'gbp', 
                        'product_data': {
                            'name': f'Consultation with {instance.name}',
                        },
                        'unit_amount': amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/payment/success/'),
                cancel_url=request.build_absolute_uri('/payment/cancel/'),
                metadata={
                    "contact_id": instance.id
                }
            )

            return redirect(checkout_session.url, code=303)

    else:
        form = ContactUs_Form()

    return render(request, "contact.html", {"form": form, "price": prices})



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ContactUs
from .email import send_mails


def payment_success_view(request):
    contact_id = request.session.get('contact_id')
    if contact_id:
        try:
            instance = ContactUs.objects.get(id=contact_id)
            if not instance.is_paid:
                instance.is_paid = True
                if instance.time:
                    instance.time.is_available = False
                    instance.time.save()

                instance.save()
                send_mails(instance)

            # ✅ Clean up session
            del request.session['contact_id']

            messages.success(request, "Payment successful! Your consultation has been confirmed.")
            return render(request, "payment_success.html", {"contact": instance})
        except ContactUs.DoesNotExist:
            messages.error(request, "We couldn't find your booking.")
    else:
        messages.error(request, "No payment session found.")

    return redirect("contact")



def payment_cancel_view(request):
    messages.warning(request, "Payment was cancelled. Your booking has not been confirmed.")
    return render(request, "payment_cancel.html")
