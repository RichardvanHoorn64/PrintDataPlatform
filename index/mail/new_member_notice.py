from django.core.mail import send_mail
from printdataplatform.settings import *


# admin mail for new members
# def new_member_confirmationmail(user):
#     try:
#         send_mail(
#             'Aanmelding nieuw account',
#             'Er is een nieuwe aanmelding op Het PrintdDataPlatform van '
#             + str(user.first_name) + ' ' + str(user.last_name)
#             + ' namens: ' + str(user.company) + ' uit ' + str(user.city) + ' email: ' + str(user.e_mail_general)
#             + ' telefoonnummer: ' + str(user.tel_general)
#             ,
#             EMAIL_HOST_USER,
#             [EMAIL_TO_ADMIN],
#             fail_silently=False,
#
#         )
#     except Exception as e:
#         print("new member confirmationmail error: ", str(e))


def new_member_notice_body(user):
    body = (
        'Aanmelding nieuw account',
        'Er is een nieuwe aanmelding op Het PrintdDataPlatform van '
        + str(user.first_name) + ' ' + str(user.last_name)
        + ' namens: ' + str(user.company) + ' uit ' + str(user.city) + ' email: ' + str(user.e_mail_general)
        + ' telefoonnummer: ' + str(user.tel_general)
    )
    return body


def new_member_confirmationmail_body(user):
    body = (
            'Beste ' + str(user.first_name) + '\n'
            + 'Bedankt voor uw aanmelding op het PrintDataPlatform, uw aanmeling wordt nog beoordeeld.'
            +  "\n" + '\n'
            + 'Aarzel niet om contact met ons op te nemen als hierover nog vragen zijn' "\n" +
            "\n" + '\n' + '\n'
            + 'Hartelijke groet, ' + '\n'
            + 'Richard van Hoorn ' + '\n'
            + 'PrintDataPlatform BV, ' + '\n'
            + 'contact@printdataplatform.nl' + '\n'
            + 'tel: 0655962062')
    return body
