from django.core.mail import send_mail
from printdataplatform.settings import EMAIL_HOST_USER, EMAIL_AANMELDEN


# admin mail for new members
def new_member_confirmationmail(user):
    try:
        send_mail(
            'Aanmelding nieuw account',
            'Er is een nieuwe aanmelding op Het PrintdDataPlatform van '
            + str(user.first_name) + ' ' + str(user.last_name)
            + ' namens: ' + str(user.company) + ' uit ' + str(user.city) + ' email: ' + str(user.e_mail_general)
            + ' telefoonnummer: ' + str(user.tel_general)
            + ' Producentaanmelding: ' + user.producerplan

            ,
            EMAIL_HOST_USER,
            [EMAIL_HOST_USER, EMAIL_AANMELDEN],
            fail_silently=False,

        )
    except Exception as e:
        print("mail error: ", str(e))
