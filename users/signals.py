from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from knox.signals import token_expired


@receiver(token_expired)
def notify_user_token_expired(sender, username: str, source: str, **kwargs):
    User = get_user_model()

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return

    to_email = getattr(user, "email", "")
    if not to_email:
        return

    current_site = Site.objects.get_current()

    context = {
        "current_site": current_site,
        "user": user,
        "username": username,
        "source": source,
    }

    subject = "Your Event Horizon API key expired"
    text_body = render_to_string("users/email/token_expired.txt", context).strip()
    html_body = render_to_string("users/email/token_expired.html", context)

    from_email = getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@eventhorizon.local")

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=[to_email],
    )
    email.attach_alternative(html_body, "text/html")
    email.send(fail_silently=True)
