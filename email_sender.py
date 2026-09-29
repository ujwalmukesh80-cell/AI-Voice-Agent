import smtplib
from email.message import EmailMessage


def send_brochure(receiver_email, pdf_file):

    sender_email = "ujwalmukesh26@gmail.com"
    app_password = "ujwal@2602"

    msg = EmailMessage()

    msg["Subject"] = "Property Brochure"
    msg["From"] = sender_email
    msg["To"] = receiver_email

    msg.set_content(
        """
Hello,

Thank you for your interest.

Please find the attached property brochure.

Regards,
Dream Homes
"""
    )

    with open(pdf_file, "rb") as f:
        msg.add_attachment(
            f.read(),
            maintype="application",
            subtype="pdf",
            filename=pdf_file
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    return True