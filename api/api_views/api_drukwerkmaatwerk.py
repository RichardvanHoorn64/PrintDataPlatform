import json
from datetime import datetime

import requests
from api.models import APIs
from django.http import JsonResponse
from offers.models import Offers
from offers.rfq_functions import *
from printdataplatform.settings import DEBUG
from printprojects.models import PrintProjects


def api_printdataplatform_com(user, offer_id):
    if DEBUG:
        printdataplatform_key = 12345
    else:
        printdataplatform_key = 'nog koppelen'
        error = 'Maak een blob opslaglocatie voor de printdataplatform_key aan'
        print(error)

    offer = Offers.objects.get(offer_id=offer_id)
    project = PrintProjects.objects.get(printproject_id=offer.printproject_id)
    productcategory_id = project.productcategory_id
    username = user.first_name + " " + user.last_name
    api = APIs.objects.model.objects.filter(member_id=user.member_id, api_producer_id=offer.producer_id).first()

    rfq = {}

    if productcategory_id == 3:  # selfcovers
        rfq = {
            "productcategory_id": productcategory_id,
            "printdataplatform_key": printdataplatform_key,
            "producent_id": api.api_producer_id,
            "klant_id": api.api_client_id,
            "username": username,
            "eigen_ordernummer": project.own_quotenumber,
            "omschrijving": project.description,
            "oplage": project.volume,
            "breedte_mm_product": project.width_mm_product,
            "hoogte_mm_product": project.height_mm_product,
            "aantal_paginas": project.number_of_pages,
            "staand_liggend": project.portrait_landscape,
            "nabewerking_brochures": project.finishing_brochures,
            "papiersoort_bw": project.paperbrand,
            "papiergewicht_m2_bw": project.paperweight,
            "papierkleur_bw": project.papercolor,
            "bedrukking_bw": project.print,
            "aantal_pms_kleuren_bw": project.number_pms_colors,
            "persvernis_bw": project.pressvarnish,
            "papiersoort_omslag": project.paperbrand_cover,
            "papiergewicht_m2_omslag": project.paperweight_cover,
            "verpakking": project.packaging,
        }

    elif productcategory_id in [4, 5]:  # brochures
        try:
            rfq = {
                "productcategory_id": productcategory_id,
                "printdataplatform_key": printdataplatform_key,
                "username": username,
                "eigen_ordernummer": project.own_quotenumber,

                "producent_id": api.api_producer_id,
                "klant_id": api.api_client_id,
                "omschrijving": project.description,
                "oplage": project.volume,
                "breedte_mm_product": project.width_mm_product,
                "hoogte_mm_product": project.height_mm_product,
                "aantal_paginas": project.number_of_pages,
                "staand_liggend": project.portrait_landscape,
                "nabewerking_brochures": project.finishing_brochures,
                "papiersoort_bw": project.paperbrand,
                "papiergewicht_m2_bw": project.paperweight,
                "papierkleur_bw": project.papercolor,
                "bedrukking_bw": project.print,
                "aantal_pms_kleuren_bw": project.number_pms_colors,
                "persvernis_bw": project.pressvarnish,
                "papiersoort_omslag": project.paperbrand_cover,
                "papiergewicht_m2_omslag": project.paperweight_cover,
                "papierkleur_omslag": project.papercolor_cover,
                "uitvoering_omslag": project.printsided_cover,
                "bedrukking_omslag": project.print_cover,
                "bedrukking_binnenzijde_omslag": project.print_rear_cover,
                "aantal_pms_kleuren_omslag": project.number_pms_colors_cover,
                "aantal_pms_kleuren_omslag_binnenzijde": project.number_pms_colors_rear_cover,
                "persvernis_omslag": project.pressvarnish_cover,
                "persvernis_omslag_binnenzijde": project.pressvarnish_rear_cover,
                "veredeling_omslag": project.enhance,
                "verpakking": project.packaging,
            }
        except Exception as e:
            error = e
            print(error)

    json_rfq = json.dumps(rfq, indent=4)

    # url = 'https://www.printdataplatform.com/api_deprintmanager'
    if not DEBUG:
        url = 'www.printdataplatform.com/api_deprintmanager/'
    else:
        url = 'http://127.0.0.1:9000/api_deprintmanager/'
    headers = {'Content-type': 'application/json'}

    try:
        rfq_response = requests.post(url, json=json_rfq, headers=headers)
        print("Status code: ", rfq_response.status_code)
        print("Status headers: ", rfq_response.headers)
        print("Status json: ", rfq_response.json())

        if rfq_response.status_code == 200:
            data = rfq_response.json()

            calculation_status = data['calculation_status']
            print('calculation_status: ', calculation_status)

            if calculation_status == 'berekend':
                print('berekend ja')
                try:
                    offer.offer = data['netto_kostentotaal']
                    offer.offer_1000extra = data['netto_totaal_1000_meer']
                    offer.producer_quote = data['offertenummer']
                    offer.producer_notes = 'API aanbieding nr ' + data['offertenummer']
                    offer.offerstatus_id = 2
                    offer.offer_date = datetime.now()
                    offer.save()
                except Exception as e:
                    error = ('offer save error: ', str(e))
                    print(error)

            if calculation_status == 'niet berekend':
                send_rfq_mail(offer.producer.company, user.member.company, offer, project)

        return JsonResponse(rfq_response.json(), safe=False)
    except Exception as e:
        print("rfq_response error: ", e)
