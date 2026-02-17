from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.conf import settings
import os


def send_email(to_email, subject, content):
    """
    Send plain-text email using SendGrid.
    This function NEVER crashes the app.
    """
    try:
        message = Mail(
            from_email=settings.DEFAULT_FROM_EMAIL,
            to_emails=to_email,
            subject=subject,
            plain_text_content=content
        )

        sg = SendGridAPIClient(os.environ.get("SENDGRID_API_KEY"))
        sg.send(message)

    except Exception as e:
        # Log only — do NOT break signup/login
        print("Email send failed:", e)