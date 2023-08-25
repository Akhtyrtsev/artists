from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

FROM_EMAIL = "wellhello@gmail.com"
# Render the HTML template


@shared_task
def send_email(subject: str, recipient_list: list, template_name: str, context: dict):
    html_message = render_to_string(template_name, context)
    plain_message = strip_tags(html_message)
    send_mail(
        subject, plain_message, FROM_EMAIL, recipient_list, html_message=html_message
    )
