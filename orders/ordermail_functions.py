from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from printprojects.models import *
from profileuseraccount.form_invalids import error_mail_admin

try:
    from printdataplatform.settings import EMAIL_HOST_USER
except:
    pass

from orders.models import Orders
from profileuseraccount.models import *


# email zenden
def send_ordermail_producer(order_id, user):  # door producent naar klant
    order = Orders.objects.get(order_id=order_id)
    member = Members.objects.get(member_id=user.member_id)
    producer = Producers.objects.get(producer_id=order.producer_id)
    orderer = UserProfile(id=order.orderer)
    productgroep = order.productgroep
    calculatie_id = order.calculatie_id
    # offerte = retrieve_calculatie(calculatie_id, productgroep)
    # offertenummer = offerte.offertenummer
    # aanvraag = Aanvragen.objects.get(offertenummer=offertenummer)

    # aflopend = []
    # bedrukking_basis = []
    # persvernis_basis = []
    # veredeling_basis = []
    # nabewerking_brochures = []
    # pms_basis = []
    # bedrukking_bw = []
    # pms_bw = []
    # persvernis_bw = []
    # vouwen = []
    # folderomvang = []
    # paginaformaatbrochures = []
    # bedrukking_omslag = []
    # pms_omslag = []
    # persvernis_omslag = []
    # veredeling_omslag = []
    #
    # if not order.klant_ordernummer or order.klant_ordernummer == 'Geen opgave':
    #     klant_ordernummer = order.ordernummer
    # else:
    #     klant_ordernummer = order.klant_ordernummer
    #
    # try:
    #     if offerte.aflopend_bedrukt == 'Ja':
    #         aflopend = 'Aflopend bedrukt'
    #     else:
    #         aflopend = 'Niet aflopend bedrukt'
    # except:
    #     pass
    #
    # try:
    #     bedrukking_basis = bedrukking_beschrijving_basis(offerte.uitvoering, offerte.bedrukking,
    #                                                      offerte.bedrukking_achterzijde)
    #     pms_basis = pms_beschrijving_basis(offerte.uitvoering, offerte.aantal_pms_kleuren,
    #                                        offerte.aantal_pms_kleuren_achterzijde)
    #     persvernis_basis = persvernis_beschrijving_basis(offerte.persvernis,
    #                                                      offerte.persvernis_achterzijde),
    #
    #     veredeling_basis = veredeling_beschrijving_plano(offerte.veredeling,
    #                                                      offerte.veredeling_achterzijde)
    # except:
    #     pass
    #
    # try:
    #     vouwen = vouwen_beschrijving(offerte.nabewerking_folders)
    #     folderomvang = aantal_paginas_folders(offerte.nabewerking_folders)
    # except:
    #     pass
    #
    # try:
    #     pms_basis = pms_beschrijving_basis(offerte.uitvoering, offerte.aantal_pms_kleuren,
    #                                        offerte.aantal_pms_kleuren_achterzijde)
    # except:
    #     pass
    #
    # try:
    #     paginaformaatbrochures = paginaformaat(offerte.breedte_mm_product, offerte.hoogte_mm_product,
    #                                            offerte.staand_liggend)
    # except:
    #     pass
    #
    #     # Context voor brochures / selfcovers
    # try:
    #     nabewerking_brochures = nabewerking_brochures_beschrijving(offerte.nabewerking_brochures)
    #     bedrukking_bw = bedrukking_beschrijving_bw(offerte.bedrukking_bw)
    #     pms_bw = pms_beschrijving_bw(offerte.aantal_pms_kleuren_bw)
    #     persvernis_bw = persvernis_beschrijving_bw(offerte.persvernis_bw)
    # except:
    #     pass
    #     # Context voor brochures omslagen
    # try:
    #     bedrukking_omslag = bedrukking_beschrijving_basis(offerte.bedrukking_omslag, offerte.bedrukking_omslag,
    #                                                       offerte.bedrukking_binnenzijde_omslag)
    #     pms_omslag = pms_beschrijving_basis(offerte.uitvoering_omslag, offerte.aantal_pms_kleuren_omslag,
    #                                         offerte.aantal_pms_kleuren_omslag_binnenzijde)
    #     persvernis_omslag = persvernis_beschrijving_basis(offerte.persvernis_omslag,
    #                                                       offerte.persvernis_omslag_binnenzijde)
    #     veredeling_omslag = veredeling_beschrijving_omslag(offerte.veredeling_omslag)
    # except:
    #     pass
    #
    # merge_data = {
    #     'klant_ordernummer': klant_ordernummer,
    #     'productgroep': productgroep,
    #     'opdracht': opdracht,
    #     'aanvraag': aanvraag,
    #     'offerte': offerte,
    #     'besteller': besteller.first_name + " " + besteller.last_name,
    #     'besteller_email': besteller.email,
    #     'klant': klant,
    #     'status': 'Aangevraagd',
    #     'gevouwen': vouwen,
    #     'aantal_paginas_folders': folderomvang,
    #     'nabewerking_brochures': nabewerking_brochures,
    #     'aflopend': aflopend,
    #     'bedrukking_bw': bedrukking_bw,
    #     'pms_bw': pms_bw,
    #     'persvernis_bw': persvernis_bw,
    #     'verpakking': offerte.verpakking,
    #     'bedrukking_basis': bedrukking_basis,
    #     'pms_basis': pms_basis,
    #     'persvernis_basis': persvernis_basis,
    #     'veredeling': veredeling_basis,
    #     'bedrukking_omslag': bedrukking_omslag,
    #     'veredeling_omslag': veredeling_omslag,
    #     'pms_omslag': pms_omslag,
    #     'persvernis_omslag': persvernis_omslag,
    #     'paginaformaatbrochures': paginaformaatbrochures,
    #     'afleveradres': bepaal_afleveradres(opdracht, user),
    # }

    merge_data = {}
    # select email template
    email_template = 'orders/emails_ordermelding/email_ordermelding.html'
    subject = render_to_string("orders/emails_ordermelding/ordermelding_subject.txt", merge_data)
    text_body = render_to_string('orders/emails_ordermelding/tekst_ordermelding.txt', merge_data)
    html_body = render_to_string(email_template, merge_data)

    from_email = EMAIL_HOST_USER
    recepients = [producer.e_mail_orders, ]

    order_mail = EmailMultiAlternatives(subject=subject, from_email=from_email,
                                        to=recepients, body=text_body)
    order_mail.attach_alternative(html_body, "text/html")
    try:
        order_mail.send()
    except Exception as e:
        error_mail_admin('order_mail.send() error: ', e)
