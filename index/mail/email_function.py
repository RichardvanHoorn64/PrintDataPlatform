# This is a sample email Python script for PrintDataPlatform.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from azure.communication.email import EmailClient


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

# def main():
#     subject = 'PrintDataPlatform offerteaanvraag'
#     address = 'info@richardvanhoorn.nl'
#     send_printdataplatform_mail(subject, address, body)
#
#
# main()
