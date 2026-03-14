import smtplib
import time
from email.message import EmailMessage
from datetime import datetime


def send_email(config, to_email, business_name):
    subject = f"Quick Introduction – {business_name}"

    body = f"""Hello {business_name},

We came across your business and would love to explore a collaboration opportunity.

We specialize in digital solutions including web, app, and AI services.

Looking forward to connecting.

Best regards,
FEAR Team
"""

    msg = EmailMessage()
    msg["From"] = config["sender_email"]
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config["sender_email"], config["sender_password"])
        server.send_message(msg)

    time.sleep(config["delay_seconds"])

    return {
        "email_sent": "YES",
        "email_subject": subject,
        "email_body": body,
        "email_sent_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
