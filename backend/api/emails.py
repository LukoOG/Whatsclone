from .models import Profile
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import random

def generate_otp(length=6):
    string = ['1','2','3','4','5','6','7','8','9','0']
    return ''.join(random.choices(string, k=length))

def send_otp_email(email):
    otp = generate_otp()
    user = Profile.objects.get(email=email)
    user.otp = otp
    user.save()
    template = render_to_string(
        'api/email.html', {'phone':user.phone, 'otp':user.otp}
    )
    email = EmailMessage(
        'your verification email',
        template,
        settings.EMAIL_HOST_USER,
        [email]
    )
    email.fail_silently = False
    email.send()

