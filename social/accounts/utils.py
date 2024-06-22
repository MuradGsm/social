from django.core.mail import EmailMultiAlternatives
from django.urls import reverse
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_verification_email(user, request):
    subject = 'Подтверждение электронной почты'
    verification_url = request.build_absolute_uri(reverse('verify_email', args=[user.email_verification_token]))
    html_content = render_to_string('email_verification.html', {'verification_link': verification_url})
    text_content = strip_tags(html_content)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    email = EmailMultiAlternatives(
        subject,
        text_content,
        email_from,
        recipient_list
    )
    email.attach_alternative(html_content, "text/html")
    email.send()