from django.core.mail import EmailMessage
from django.template.loader import render_to_string


### fonction d'envoi de l'email au client 
def envoyer_email(commande, destinataire_email, pdf_path):
    subject = f"Confirmation de votre commande - {commande.matricule_commande}"
    message = render_to_string('email_confirmation.html', {
        'commande': commande
    })

    email = EmailMessage(
        subject,
        message,
        to=[destinataire_email]

    )

    email.content_subtype = "html"

    # Attacher le PDF de la facture si dispo
    if pdf_path:
        email.attach_file(pdf_path)

    email.send()




