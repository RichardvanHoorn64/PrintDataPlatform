from index.mail.email_function import send_printdataplatform_mail
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
        'offer_key': str(offer.offer_key),
        'printproject': printproject,
    }

    # select email template
    email_template = 'offers/emails_rfq/rfq_mailbody.html'
    subject = render_to_string("offers/emails_rfq/rfq_subject.txt", merge_data)
    html_body = render_to_string(email_template, merge_data)
    address = producer.e_mail_rfq

    try:
        send_printdataplatform_mail(subject, address, html_body)
    except Exception as e:
        error_mail_admin('rfq_mail.send() error: ', e)

