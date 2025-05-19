from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_mails(instance):
    customer_subject = "Your DietLab Consultation Has Been Successfully Booked!"
    owner_subject = f"New Consultation Booking - {instance.name}"

    # Plain text for customer
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

    # HTML for customer
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

                <p>💷 <strong>Consultation Fee:</strong> {instance.price}</p>
                <p>🧑 <strong>Name:</strong> {instance.name}</p>
                <p>🎂 <strong>Age:</strong> {instance.age}</p>
                <p>📧 <strong>Email:</strong> {instance.email}</p>
                <p>📞 <strong>Phone:</strong> <a href="tel:{instance.phone}" style="color: #0D47A1;">{instance.phone}</a></p>
                <p>🎯 <strong>Health Goals:</strong> {instance.goal}</p>
                <p>⚠️ <strong>Medical History:</strong> {instance.any_medical_history}</p>
                <p>📝 <strong>Medical Details:</strong> {instance.medical_history_details or 'None provided'}</p>

                <p style="color: #D32F2F; line-height: 1.6;">
                    <strong>Note:</strong> The time shown is in UK time (GMT/BST). If you're in a different country, please check your local time using the converter below. 
                    <strong>Forgot the time you booked?</strong> No worries! You can double-check the correct time for your location using 
                    <a href="https://www.timeanddate.com/worldclock/converter.html?iso=20250506T090000&p1=176&p2=776&p3=136" 
                    style="color: #0D47A1; text-decoration: none;" target="_blank">World Time Buddy</a>.
                </p>

                <p>📅 <strong>Appointment Date:</strong> {instance.time.date}</p>
                <p>🕒 <strong>Appointment Time:</strong> {instance.time}</p>

                <p style="margin-top: 20px; color: #666;">We look forward to helping you achieve your health goals!</p>
            </div>
        </div>
    </body>
</html>
"""

    # Owner plain text
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

    # Owner HTML
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

    # Send customer email
    customer_email = EmailMultiAlternatives(
        customer_subject,
        customer_text_content,
        settings.DEFAULT_FROM_EMAIL,
        [instance.email],
    )
    customer_email.attach_alternative(customer_html_content, "text/html")
    customer_email.send()

    # Send owner email
    owner_email = EmailMultiAlternatives(
        owner_subject,
        owner_text_content,
        settings.DEFAULT_FROM_EMAIL,
        [settings.CONTACT_EMAIL],
    )
    owner_email.attach_alternative(owner_html_content, "text/html")
    owner_email.send()
