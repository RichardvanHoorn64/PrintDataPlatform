from printdataplatform.settings import DEBUG
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from profileuseraccount.form_invalids import error_mail_admin

try:
    from printdataplatform.settings import *
finally:
    pass


# send rfq to selected producers
def send_rfq_mail(producer, member_company, offer, printproject):
    merge_data = {
        'producer': producer,
        'member_company': member_company,
        'offer': offer,
        'printproject': printproject,
    }

    # select email template
    email_template = 'offers/emails_rfq/rfq_mailbody.html'
    subject = render_to_string("offers/emails_rfq/rfq_subject.txt", merge_data)
    text_body = render_to_string('offers/emails_rfq/rfq_text.txt', merge_data)
    html_body = render_to_string(email_template, merge_data)

    from_email = EMAIL_TO_USERS
    if DEBUG:
        recepients = ["info@richardvanhoorn.nl", ]
    else:
        recepients = [producer.e_mal_general, ]

    rfq_mail = EmailMultiAlternatives(subject=subject, from_email=from_email,
                                      to=recepients, body=text_body)
    rfq_mail.attach_alternative(html_body, "text/html")
    try:
        rfq_mail.send()
    except Exception as e:
        error_mail_admin('rfq_mail.send() error: ', e)
