# This is a sample email Python script for PrintDataPlatform.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from azure.communication.email import EmailClient

# body = """
# <style>
#     p {
#         font-family: 'Courier New', monospace;;
#     }
#
#     table {
#         font-family: 'Courier New', monospace;;
#         border-collapse: collapse;
#     }
#
#     td, th {
#         border: 1px solid #dddddd;
#         text-align: left;
#         padding: 8px;
#     }
#
# </style>
# <html>
# <body>
# <p>
#     Hallo,<br><br>
#     Op het PrintDataPlatform heeft requester namens member_company
#     voor company een offerteaanvraag voor 100 ex.project_title gedaan.
#     <br><br>
#     Bekijk en beantwoord de offerteaanvraag op: <a
#         href="https://printdataplatform.com/{% url 'offer_producers_form' offer.offer_id %}">https://printdataplatform.com/offer_producers_form/12</a>,
#     <br><br>
#     Open de aanvraag met deze unieke toegangscode: {{ offer.offer_key }}
#     <br><br>
#     Hartelijke groet,<br>
#     Richard van Hoorn
#     <br>
#     <a href="https://printdataplatform.com/">PrintDataPlatform BV</a>
#     <br>
#     mail: contact@printdataplatform.nl
#     <br>
#     tel: 06-55962062
#
# <img src="cid:my_inline_image_2" alt="my_inline_image_2" />
# <br><br>
# </p>
# </body>
# </html>
# """


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
        print('mail error: ',str(subject), str(address), str(e))


# def main():
#     subject = 'PrintDataPlatform offerteaanvraag'
#     address = 'info@richardvanhoorn.nl'
#     send_printdataplatform_mail(subject, address, body)
#
#
# main()
