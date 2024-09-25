from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from offers.models import Offers
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
    order_id = order.order_id
    offer_id = Orders.objects.get(order_id=order_id)
    offer = Offers.objects.get(offer_id=offer_id)
    printproject_id = offer.printproject_id
    member = Members.objects.get(member_id=order.member_id)
    producer = Producers.objects.get(producer_id=order.producer_id)
    orderer = UserProfile(id=order.orderer)
    productgroep = order.productgroep
    calculatie_id = order.calculatie_id

    offernummer = offer.offernummer
    # aanvraag = Aanvragen.objects.get(offernummer=offernummer)

    aflopend = []
    bedrukking_basis = []
    persvernis_basis = []
    veredeling_basis = []
    nabewerking_brochures = []
    pms_basis = []
    bedrukking_bw = []
    pms_bw = []
    persvernis_bw = []
    vouwen = []
    folderomvang = []
    paginaformaatbrochures = []
    bedrukking_omslag = []
    pms_omslag = []
    persvernis_omslag = []
    veredeling_omslag = []

    # if not order.klant_ordernummer or order.klant_ordernummer == 'Geen opgave':
    #     klant_ordernummer = order.ordernummer
    # else:
    #     klant_ordernummer = order.klant_ordernummer
    #
    # try:
    #     bedrukking_basis = bedrukking_beschrijving_basis(offer.uitvoering, offer.bedrukking,
    #                                                      offer.bedrukking_achterzijde)
    #     pms_basis = pms_beschrijving_basis(offer.uitvoering, offer.aantal_pms_kleuren,
    #                                        offer.aantal_pms_kleuren_achterzijde)
    #     persvernis_basis = persvernis_beschrijving_basis(offer.persvernis,
    #                                                      offer.persvernis_achterzijde),
    #
    #     veredeling_basis = veredeling_beschrijving_plano(offer.veredeling,
    #                                                      offer.veredeling_achterzijde)
    # except:
    #     pass
    #
    # try:
    #     vouwen = vouwen_beschrijving(offer.nabewerking_folders)
    #     folderomvang = aantal_paginas_folders(offer.nabewerking_folders)
    # except:
    #     pass
    #
    # try:
    #     pms_basis = pms_beschrijving_basis(offer.uitvoering, offer.aantal_pms_kleuren,
    #                                        offer.aantal_pms_kleuren_achterzijde)
    # except:
    #     pass
    #
    # try:
    #     paginaformaatbrochures = paginaformaat(offer.breedte_mm_product, offer.hoogte_mm_product,
    #                                            offer.staand_liggend)
    # except:
    #     pass
    #
    #     # Context voor brochures / selfcovers
    # try:
    #     nabewerking_brochures = nabewerking_brochures_beschrijving(offer.nabewerking_brochures)
    #     bedrukking_bw = bedrukking_beschrijving_bw(offer.bedrukking_bw)
    #     pms_bw = pms_beschrijving_bw(offer.aantal_pms_kleuren_bw)
    #     persvernis_bw = persvernis_beschrijving_bw(offer.persvernis_bw)
    # except:
    #     pass
    #     # Context voor brochures omslagen
    # try:
    #     bedrukking_omslag = bedrukking_beschrijving_basis(offer.bedrukking_omslag, offer.bedrukking_omslag,
    #                                                       offer.bedrukking_binnenzijde_omslag)
    #     pms_omslag = pms_beschrijving_basis(offer.uitvoering_omslag, offer.aantal_pms_kleuren_omslag,
    #                                         offer.aantal_pms_kleuren_omslag_binnenzijde)
    #     persvernis_omslag = persvernis_beschrijving_basis(offer.persvernis_omslag,
    #                                                       offer.persvernis_omslag_binnenzijde)
    #     veredeling_omslag = veredeling_beschrijving_omslag(offer.veredeling_omslag)
    # except:
    #     pass
    #
    # merge_data = {
    #     'klant_ordernummer': klant_ordernummer,
    #     'productgroep': productgroep,
    #     'opdracht': opdracht,
    #     'aanvraag': aanvraag,
    #     'offer': offer,
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
    #     'verpakking': offer.verpakking,
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
    email_template = 'orders/ordermail_includes/email_order_notice.html'
    subject = render_to_string("orders/ordermail_includes/order_notice_subject.txt", merge_data)
    text_body = render_to_string('orders/ordermail_includes/text_order_notice.txt', merge_data)
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
