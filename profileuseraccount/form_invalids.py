from django.core.mail import send_mail
from printdataplatform.settings import *


def form_invalid_message(form, response):
    if DEBUG:
        print('Form invalid:', "form is invalid error :" + str(response) + "form errors :" + str(
            form.errors) + "form cleaned_data :" + str(form.cleaned_data))
    else:
        try:
            send_mail('Form invalid:', "form is invalid, response :" + str(response) + "form errors :" + str(
                form.errors) + "form cleaned_data :" + str(form.cleaned_data), EMAIL_HOST_USER,
                      [EMAIL_TO_ADMIN], fail_silently=False, )
        except Exception as e:
            print('Form invalid:', "form is invalid error :" + str(response) + "form errors :" + str(
                form.errors) + "form cleaned_data :" + str(form.cleaned_data), str(e))


def error_mail_admin(error_type, error):
    try:
        send_mail('Error message:', "Error type:" + error_type + "Error:" + str(error), EMAIL_HOST_USER,
                  [EMAIL_TO_ADMIN], fail_silently=False, )
    except Exception as e:
        print('Error message:', "Error type:" + error.type + "Error:" + str(error), str(e))
