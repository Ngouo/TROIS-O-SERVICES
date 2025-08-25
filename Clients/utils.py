from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def relance_email(destinataire_email):
    subject = f"Relance concernant votre Commande"
    message = render_to_string('relance.html')

    email = EmailMessage(
        subject,
        message,
        to = [destinataire_email],
    )

    email.content_subtype = "html"
    email.send()