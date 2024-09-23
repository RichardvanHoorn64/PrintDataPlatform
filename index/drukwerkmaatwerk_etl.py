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
        # load_printprojects_veldhuis(self.inputfolder, 'printprojects_veldhuis.csv')
        # load_offers_veldhuis(self.inputfolder, 'offers_veldhuis.csv')

        return redirect('/home/')


# load drukwerkmaatwerk_klanten_veldhuis
def load_klanten_veldhuis(inputfolder, inputfile, request):
    try:
        with open(inputfolder + inputfile, 'r') as klanten_veldhuis_csv_file:
            klanten_veldhuis = pd.read_csv(klanten_veldhuis_csv_file, delimiter=',', header=0, encoding="utf-8")
            klanten_veldhuis_oud = Members.objects.filter(exclusive_producer_id=2, member_plan_id=3)
            klanten_veldhuis_oud.delete()

            for index, row in klanten_veldhuis.iterrows():
                veldhuis_klant = Members(
                    member_id=row['klant_id'],
                    company=row['bedrijfsnaam'],
                    user_admin=row['user_admin'],
                    exclusive_producer_id=2,
                    manager=row['manager'],
                    tel_general=row['telefoonnummer_algemeen'],
                    e_mail_general=row['e_mail_algemeen'],
                    street_number=row['straat_huisnummer'],
                    postal_code=row['postcode'],
                    city=row['plaats'],
                    demo_company=False,
                    member_plan_id=3,
                    language_id=1,
                    active=True,
                    country_code='nl',
                    created=row['created'],
                )
                veldhuis_klant.save()
        print('drukwerkmaatwerk klanten veldhuis loaded')
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
                    veldhuis_match.save()

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
                veldhuis_user.save()
        print('drukwerkmaatwerk users veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk users veldhuis load: ', str(e))


# load drukwerkmaatwerk_printproject_veldhuis
def load_printprojects_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            printprojects_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                                           encoding="utf-8")
            printprojects_veldhuis_oud = PrintProjects.objects.filter(producer_id=2, productcategory_id=3,
                                                                                assortiment_item=False)
            printprojects_veldhuis_oud.delete()

            # klant_id,producent_id,perc_korting_tw_brochures_gebonden,manager,user_admin,bedrijfsnaam,telefoonnummer_algemeen,e_mail_algemeen,straat_huisnummer,postcode,plaats,actief,is_welkom,perc_korting_tw_brochures_gehecht,perc_korting_tw_folders,perc_korting_tw_plano,perc_korting_tw_selfcovers,perc_korting_tw_sheets,created,
            # perc_korting_tw_enveloppen,eigen_offertetemplate,locatie_offertetemplate,perc_korting_tw_brochures_garenloos
            for index, row in printprojects_veldhuis.iterrows():

                aanvraag_status = 2
                if row['aanvraag_status'] == 'Order':
                    aanvraag_status = 3

                persvernis_bw = 0
                if row['persvernis_bw'] == 'Ja':
                    persvernis_bw = 1

                new_printproject = PrintProjects(
                    printproject_id=row['aanvragen_id'],
                    offer_date=row['aanvraag_datum'],
                    description=row['omschrijving'],
                    requester=row['user_id'],
                    producer_id=2,
                    member_id=row['klant_id'],
                    productcategory_id=3,
                    offer=row['offer_id'],
                    project_title=row['omschrijving'],
                    volume=row['oplage'],
                    height_mm_product=row['hoogte_mm_product'],
                    width_mm_product=row['breedte_mm_product'],
                    paperbrand=row['papiersoort_bw'],
                    paperweight=row['papiergewicht_m2_bw'],
                    papercolor=row['papierkleur_bw'],
                    printsided=modify_printsided(row['printsided']),
                    pressvarnish_front=modify_boleaninput(row['pressvarnish_front']),
                    pressvarnish_rear=modify_boleaninput(row['pressvarnish_rear']),
                    pressvarnish_booklet=persvernis_bw,
                    enhance_sided=modify_printsided(row['enhance_sided']),
                    enhance_front=find_enhancement_id(row['enhance_front']),
                    enhance_rear=find_enhancement_id(row['enhance_rear']),
                    packaging=find_packaging_id(row['verpakking']),
                    # folding=find_foldingspecs(row['folding']),
                    number_of_pages=row['aantal_paginas'],
                    portrait_landscape=find_orientation(row['staand_liggend']),
                    finishing_brochures=find_brochure_finishingmethod_id(row['nabewerking_brochures']),
                    # print_front=modify_printcolors(row['print_front']),
                    # print_rear=modify_printcolors(row['print_rear']),
                    print_booklet=modify_printcolors(row['bedrukking_bw']),
                    number_pms_colors_front=0,
                    number_pms_colors_rear=0,
                    number_pms_colors_booklet=0,
                    # paperbrand_cover=row['paperbrand_cover'],
                    # paperweight_cover=row['paperweight_cover'],
                    # papercolor_cover=row['papercolor_cover'],
                    upload_date=timezone.now().today().date(),
                    assortiment_item=False,
                    printprojectstatus_id=aanvraag_status,
                    created=row['aanvraag_datum'],
                )
                # new_printproject.save()

        print('drukwerkmaatwerk printprojects veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk printprojects veldhuis load: ', str(e))


def load_offers_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            offers_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                                    encoding="utf-8")
            offers_veldhuis_oud = Offers.objects.filter(producer_id=2, productcategory_id=3)
            offers_veldhuis_oud.delete()

            # klant_id,producent_id,perc_korting_tw_brochures_gebonden,manager,user_admin,bedrijfsnaam,telefoonnummer_algemeen,e_mail_algemeen,straat_huisnummer,postcode,plaats,actief,is_welkom,perc_korting_tw_brochures_gehecht,perc_korting_tw_folders,perc_korting_tw_plano,perc_korting_tw_selfcovers,perc_korting_tw_sheets,created,
            # perc_korting_tw_enveloppen,eigen_offertetemplate,locatie_offertetemplate,perc_korting_tw_brochures_garenloos
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
                    producer_id=row['producent_id'],
                    member_id=row['klant_id'],
                    productcategory_id=3,
                    offer=row['netto_kostentotaal'],
                    offer1000extra=row['netto_totaal_1000_meer'],
                    offerstatus_id=offerstatus,
                    active=True,
                    created=row['aanvraag_datum'],
                    language_id=1
                )
                # new_offer.save()

        print('drukwerkmaatwerk selfcover offers veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk selfcover offers veldhuis load: ', str(e))


