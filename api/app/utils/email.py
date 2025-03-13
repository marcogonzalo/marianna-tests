import logging
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from fastapi import HTTPException
import os


def send_email(recipients: str | list[str], subject: str, content: str):
    """
    Send an email using SMTP
    """
    # Get email configuration from environment variables
    email_server = os.getenv("EMAIL_SERVER", "smtp.gmail.com")
    email_port = int(os.getenv("EMAIL_PORT", "587"))
    email_username = os.getenv("EMAIL_USERNAME")
    email_password = os.getenv("EMAIL_PASSWORD")
    from_email = os.getenv("FROM_EMAIL", email_username)

    if not all([email_username, email_password]):
        raise HTTPException(
            status_code=500,
            detail="Email configuration is not properly set up"
        )

    # Create message
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = recipients
    message["Subject"] = subject

    # Add body
    body = content + """
    <p>Best regards,</p>
    <p>The Hazelton Clinic</p>
    <p><a href="https://hazelton.ie"><img src="https://hazelton.ie/wp-content/uploads/2024/07/15-year-anniversary-logo-2024-copy.jpeg" alt="Hazelton Clinic" style="width: 200px; height: auto;"></a></p>
    """
    message.attach(MIMEText(body, "html", "utf-8"))

    try:
        # Create SMTP session
        with smtplib.SMTP_SSL(email_server, email_port) as server:
            server.login(email_username, email_password)
            server.send_message(message)
    except Exception as e:
        logging.error("Error sending email", e)
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send email: {str(e)}"
        )
