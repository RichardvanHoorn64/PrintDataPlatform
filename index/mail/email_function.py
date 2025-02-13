# This is a sample email Python script for PrintDataPlatform.
from azure.communication.email import EmailClient
from django.core.mail import send_mail
from printdataplatform.settings import EMAIL_TO_ADMIN, SERVER_EMAIL

# from index.mail.email_function import send_testmail
# send_testmail('Hallo')

from django.core.mail import mail_admins


def mail_admin_function():
    subject = "Belangrijke melding"
    message = "Er is een kritieke fout opgetreden in het systeem."

    mail_admins(
        subject=subject,
        message=message,
        fail_silently=False  # Zorgt ervoor dat een fout wordt gegenereerd als de e-mail niet wordt verzonden
    )


def send_testmail(bericht):
    send_mail(
        "testmail",
        bericht,
        SERVER_EMAIL,
        EMAIL_TO_ADMIN,
        fail_silently=False,
)

def send_printdataplatform_mail(subject, address, body):
    try:
        connection_string = ("endpoint=https://printdatacommunications.europe.communication.azure.com/;accesskey"
                             "=3h3Y032ISTU5egj6Sh2hb5tTzoJHx9vxdgZUkZF8NJQrRHKSL72uJQQJ99AJACULyCpj8iiDAAAAAZCS6tjg")

        client = EmailClient.from_connection_string(connection_string)

        message = {
            "senderAddress": "DoNotReply@printdataplatform.com",
            "recipients": {
                "to": [{"address": str(address)}]
            },
            "content": {
                "subject": str(subject),
                "html": str(body),
            },
        }
        client.begin_send(message)
    except Exception as e:
        print('mail error: ', str(subject), str(address), str(e))

