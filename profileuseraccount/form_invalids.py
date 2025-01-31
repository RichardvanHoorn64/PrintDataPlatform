from django.core.mail import send_mail
from index.mail.email_function import send_printdataplatform_mail
from printdataplatform.settings import *


def form_invalid_message(form, response):
    if DEBUG:
        print('Form invalid:', "form is invalid error :" + str(response) + "form errors :" + str(
            form.errors) + "form cleaned_data :" + str(form.cleaned_data))
    else:
        try:
            subject = 'PrintDataPlatform Form invalid error'
            address = EMAIL_TO_ADMIN
            html_body = 'Form invalid:', "form is invalid, response :" + str(response) + "form errors :" + str(
                form.errors) + "form cleaned_data :" + str(form.cleaned_data)
            send_printdataplatform_mail(subject, address, html_body)
        except Exception as e:
            print('Form invalid:', "form is invalid error :" + str(response) + "form errors :" + str(
                form.errors) + "form cleaned_data :" + str(form.cleaned_data), str(e))


def error_mail_admin(error_type, error):
    try:
        subject = 'PrintDataPlatform error mail admin'
        address = EMAIL_TO_ADMIN
        html_body = 'Error message:', "Error type:" + error_type + "Error:" + str(error)
        send_printdataplatform_mail(subject, address, html_body)
    except Exception as e:
        print('Error message:', "Error type:" + error.type + "Error:" + str(error), str(e))



