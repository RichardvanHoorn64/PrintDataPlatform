import pandas as pd

from index.translate_functions import *
from offers.models import Offers
from printprojects.models import *
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import *
from django.shortcuts import redirect


class LoadVeldhuisDataView(LoginRequiredMixin, View):
    inputfolder = 'C:/Users/richa/Documents/0 PrintDataPlatform/load_veldhuis_data/'

    def dispatch(self, request, *args, **kwargs):
        # load_klanten_veldhuis(self.inputfolder, 'drukwerkmaatwerk_klanten_veldhuis.csv', request)
        # load_users_veldhuis(self.inputfolder, 'drukwerkmaatwerk_users_veldhuis.csv')

        # delete old printprojects
        # printprojects_veldhuis_oud = PrintProjects.objects.filter(producer_id=2, productcategory_id__in=[3, 4, 5],
        #                                                           assortiment_item=False)
        # printprojects_veldhuis_oud.delete()
        #
        # offers_veldhuis_oud = Offers.objects.filter(producer_id=2, productcategory_id__in=[3, 4, 5])
        # offers_veldhuis_oud.delete()
        #
        # # selfcovers
        # load_printprojects_veldhuis(self.inputfolder, 'selfcovers_printprojects_veldhuis.csv')
        # load_offers_veldhuis(self.inputfolder, 'selfcovers_printprojects_veldhuis.csv')
        #
        # # brochures
        # load_printprojects_veldhuis(self.inputfolder, 'brochures_printprojects_veldhuis.csv')
        # load_offers_veldhuis(self.inputfolder, 'brochures_printprojects_veldhuis.csv')

        return redirect('/home/')


# load drukwerkmaatwerk_klanten_veldhuis
def load_klanten_veldhuis(inputfolder, inputfile, request):
    try:
        with open(inputfolder + inputfile, 'r') as klanten_veldhuis_csv_file:
            # klanten_veldhuis = pd.read_csv(klanten_veldhuis_csv_file, delimiter=',', header=0, encoding="utf-8")
            klanten_veldhuis_oud = Members.objects.filter(exclusive_producer_id=2, member_plan_id=3).exclude(member_id=6).exclude(member_id=7)
            klanten_veldhuis_oud.delete()
            klanten_veldhuis_oud.delete()

        #     for index, row in klanten_veldhuis.iterrows():
        #         veldhuis_klant = Members(
        #             member_id=row['klant_id'],
        #             company=row['bedrijfsnaam'],
        #             user_admin=row['user_admin'],
        #             exclusive_producer_id=2,
        #             manager=row['manager'],
        #             tel_general=row['telefoonnummer_algemeen'],
        #             e_mail_general=row['e_mail_algemeen'],
        #             street_number=row['straat_huisnummer'],
        #             postal_code=row['postcode'],
        #             city=row['plaats'],
        #             demo_company=False,
        #             member_plan_id=3,
        #             language_id=1,
        #             active=True,
        #             country_code='nl',
        #             created=row['created'],
        #         )
        #         try:
        #             veldhuis_klant.save()
        #         except Exception as e:
        #             print('error drukwerkmaatwerk klant load: ', str(e))
        # print('drukwerkmaatwerk klanten veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk_klanten_veldhuis load: ', str(e))

    # perc_korting_tw_brochures_gehecht
    try:
        with open(inputfolder + inputfile, 'r') as klanten_veldhuis_csv_file:
            tariffs_veldhuis = pd.read_csv(klanten_veldhuis_csv_file, delimiter=',', header=0, encoding="utf-8")

            for index, row in tariffs_veldhuis.iterrows():
                try:
                    member = MemberProducerMatch.objects.get(producer_id=2, member_id=row['klant_id'])
                    member(
                        perc_salesallowance_3=row['perc_korting_tw_brochures_gehecht'],
                        perc_salesallowance_4=row['perc_korting_tw_brochures_gehecht'],
                        perc_salesallowance_5=row['perc_korting_tw_brochures_gebonden'],
                    )
                    member.save()
                except MemberProducerMatch.DoesNotExist:
                    veldhuis_match = MemberProducerMatch(
                        producer_id=2,
                        member_id=row['klant_id'],
                        memberproducerstatus_id=2,
                        perc_salesallowance_3=row['perc_korting_tw_brochures_gehecht'],
                        perc_salesallowance_4=row['perc_korting_tw_brochures_gehecht'],
                        perc_salesallowance_5=row['perc_korting_tw_brochures_gebonden'],
                    )
                    try:
                        veldhuis_match.save()
                    except Exception as e:
                        print('error drukwerkmaatwerk match load: ', str(e))

        print('drukwerkmaatwerk tariffs veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk tariffs veldhuis load: ', str(e))


# load drukwerkmaatwerk_users_veldhuis
def load_users_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as users_veldhuis_csv_file:
            users_veldhuis = pd.read_csv(users_veldhuis_csv_file, delimiter=',', header=0,
                                         encoding="utf-8")
            users_veldhuis_oud = UserProfile.objects.filter(producer_id=2, is_superuser=False, member_plan_id=3)
            users_veldhuis_oud.delete()

            for index, row in users_veldhuis.iterrows():
                member_plan_id = 3
                if row['user_type'] == 2:
                    member_plan_id = 4

                veldhuis_user = UserProfile(
                    id=row['id'],
                    member_id=row['klant_id'],
                    producer_id=row['producent_id'],
                    password=row['password'],
                    username=row['username'],
                    gender=row['man_vrouw'],
                    first_name=row['first_name'],
                    last_name=row['last_name'],
                    email=row['email'],
                    jobtitle=row['functie'],
                    mobile_number=row['mobiel_telefoonnummer'],
                    tel_general=row['algemeen_telefoonnummer'],
                    e_mail_general=row['e_mail_algemeen'],
                    street_number=row['straat_huisnummer'],
                    postal_code=row['postcode'],
                    city=row['plaats'],
                    member_plan_id=member_plan_id,
                    language_id=1,
                    active=True,
                    country_code='nl',
                    last_login=row['last_login'],
                    is_superuser=False,
                    created=row['created'],
                    modified=row['modified'],
                )
                try:
                    veldhuis_user.save()
                except Exception as e:
                    print('error drukwerkmaatwerk user load: ', str(e))
        print('drukwerkmaatwerk users veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk users veldhuis load: ', str(e))


# load drukwerkmaatwerk_printproject_veldhuis
def load_printprojects_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            printprojects_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                                 encoding="utf-8")

            for index, row in printprojects_veldhuis.iterrows():

                aanvraag_status = 2
                if row['aanvraag_status'] == 'Order':
                    aanvraag_status = 3

                new_printproject = PrintProjects(
                    producer_id=2,
                    printproject_id=row['aanvragen_id'],
                    rfq_date=row['aanvraag_datum'],
                    description=row['omschrijving'],

                    own_quotenumber=row['eigen_ordernummer'],
                    member_id=row['klant_id'],
                    productcategory_id=row['productcategory_id'],

                    project_title=row['omschrijving'],
                    volume=row['oplage'],

                    height_mm_product=row['hoogte_mm_product'],
                    width_mm_product=row['breedte_mm_product'],

                    paperbrand=row['papiersoort_bw'],
                    paperweight=row['papiergewicht_m2_bw'],
                    papercolor=row['papierkleur_bw'],

                    paperbrand_cover=row['papiersoort_omslag'],
                    paperweight_cover=row['papiergewicht_m2_omslag'],
                    papercolor_cover=['papierkleur_omslag'],

                    printsided=modify_printsided(row['uitvoering_omslag']),
                    pressvarnish_front=modify_boleaninput(row['persvernis_omslag']),
                    pressvarnish_rear=modify_boleaninput(row['persvernis_omslag_binnenzijde']),
                    pressvarnish_booklet=modify_boleaninput(row['persvernis_bw']),

                    enhance_sided=1,
                    enhance_front=find_enhancement_id(row['veredeling_omslag']),
                    enhance_rear=0,

                    folding=0,
                    packaging=find_packaging_id(row['verpakking']),

                    number_of_pages=row['aantal_paginas'],
                    portrait_landscape=find_orientation(row['staand_liggend']),
                    finishing_brochures=find_brochure_finishingmethod_id(row['nabewerking_brochures']),

                    print_front=modify_printcolors(row['bedrukking_omslag']),
                    print_rear=modify_printcolors(row['bedrukking_binnenzijde_omslag']),
                    print_booklet=modify_printcolors(row['bedrukking_bw']),
                    number_pms_colors_front=0,
                    number_pms_colors_rear=0,
                    number_pms_colors_booklet=0,

                    upload_date=timezone.now().today().date(),
                    assortiment_item=False,
                    printprojectstatus_id=aanvraag_status,
                    created=row['aanvraag_datum'],

                )
                try:
                    new_printproject.save()
                except Exception as e:
                    print('error drukwerkmaatwerk printprojects load: ', str(e))

        print('drukwerkmaatwerk printprojects veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk printprojects veldhuis load: ', str(e))


def load_offers_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            offers_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                          encoding="utf-8")

            for index, row in offers_veldhuis.iterrows():

                offerstatus = 2
                if row['aanvraag_status'] == 'Order':
                    offerstatus = 3

                persvernis_bw = 0
                if row['persvernis_bw'] == 'Ja':
                    persvernis_bw = 1

                new_offer = Offers(
                    printproject_id=row['aanvragen_id'],
                    offer_date=row['aanvraag_datum'],
                    description=row['omschrijving'],
                    requester=row['user_id'],
                    producer_id=2,
                    member_id=row['klant_id'],
                    productcategory_id=3,
                    offer=row['netto_kostentotaal'],
                    offer1000extra=row['netto_totaal_1000_meer'],
                    offerstatus_id=offerstatus,
                    active=True,
                    created=row['aanvraag_datum'],
                    language_id=1
                )
                try:
                    new_offer.save()
                except Exception as e:
                    print('error drukwerkmaatwerk offers load: ', str(e))


        print('drukwerkmaatwerk selfcover offers veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk selfcover offers veldhuis load: ', str(e))
