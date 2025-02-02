# This is a sample email Python script for PrintDataPlatform.
from azure.communication.email import EmailClient
# from printdataplatform.settings import AZURE_COMMUNICATION_STRING


def send_printdataplatform_mail(subject, address, body):
    try:
        connection_string = ("endpoint=https://printdatacommunications.europe.communication.azure.com/;accesskey"
                             "=3h3Y032ISTU5egj6Sh2hb5tTzoJHx9vxdgZUkZF8NJQrRHKSL72uJQQJ99AJACULyCpj8iiDAAAAAZCS6tjg")

        # connection_string = AZURE_COMMUNICATION_STRING
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

