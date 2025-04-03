import os
from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from app.config import (SMTP_SERVER,
                        SMTP_PORT,
                        SMTP_FROM,
                        SMTP_USERNAME,
                        SMTP_PASSWORD,
                        SERVER,
                        SERVER_PORT,
                        DEBUG)
from app.celery import celery

TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "email_templates/confirmation.html")


@celery.task
def send_confirmation_email(to_email, token):
    """Send the email confirmation with a token."""
    EMAIL_SUBJECT_CONFIRMATION = "Confirm your email at Plattr"

    if DEBUG:
        confirmation_link = f"http://{SERVER}:{SERVER_PORT}/auth/confirm/{token}"
    else:
        confirmation_link = f"https://{SERVER}:{SERVER_PORT}/auth/confirm/{token}"

    try:
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as file:
            html_template = file.read()
    except Exception as e:
        print(f"Error loading email template: {e}")
        return

    html_content = html_template.replace("{{ confirmation_link }}", confirmation_link)

    msg = MIMEMultipart()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = EMAIL_SUBJECT_CONFIRMATION
    msg.attach(MIMEText(html_content, "html"))  # Attach HTML content

    try:
        with SMTP(SMTP_SERVER, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
            smtp.sendmail(SMTP_FROM, to_email, msg.as_string())
    except Exception as e:
        print(f"Error sending email: {e}")