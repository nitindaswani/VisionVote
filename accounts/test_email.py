from django.core.mail import send_mail

send_mail(
    subject='Vision Vote Test',
    message='Email configuration working.',
    from_email=None,
    recipient_list=[
        'YOUR_EMAIL@gmail.com'
    ]
)