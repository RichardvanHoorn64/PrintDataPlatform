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

        load_klanten_veldhuis(self.inputfolder, 'drukwerkmaatwerk_klanten_veldhuis.csv', request)
        load_users_veldhuis(self.inputfolder, 'drukwerkmaatwerk_users_veldhuis.csv')
        load_selfcover_printprojects_veldhuis(self.inputfolder, 'selfcover_printprojects_veldhuis.csv')
        load_selfcover_offers_veldhuis(self.inputfolder, 'selfcover_printprojects_veldhuis.csv')
        # load_selfcover_calculations_veldhuis(self.inputfolder, 'selfcover_printprojects_veldhuis.csv')

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
            users_veldhuis_oud = UserProfile.objects.filter(producer_id=2, is_superuser=False)
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
def load_selfcover_printprojects_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            selfcover_printprojects_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                                           encoding="utf-8")
            selfcover_printprojects_veldhuis_oud = PrintProjects.objects.filter(producer_id=2, productcategory_id=3,
                                                                                assortiment_item=False)
            selfcover_printprojects_veldhuis_oud.delete()

            # klant_id,producent_id,perc_korting_tw_brochures_gebonden,manager,user_admin,bedrijfsnaam,telefoonnummer_algemeen,e_mail_algemeen,straat_huisnummer,postcode,plaats,actief,is_welkom,perc_korting_tw_brochures_gehecht,perc_korting_tw_folders,perc_korting_tw_plano,perc_korting_tw_selfcovers,perc_korting_tw_sheets,created,
            # perc_korting_tw_enveloppen,eigen_offertetemplate,locatie_offertetemplate,perc_korting_tw_brochures_garenloos
            for index, row in selfcover_printprojects_veldhuis.iterrows():

                aanvraag_status = 2
                if row['aanvraag_status'] == 'Order':
                    aanvraag_status = 3

                persvernis_bw = 0
                if row['persvernis_bw'] == 'Ja':
                    persvernis_bw = 1

                new_selfcover_printproject = PrintProjects(
                    printproject_id=row['aanvragen_id'],
                    offer_date=row['aanvraag_datum'],
                    description=row['omschrijving'],
                    requester=row['user_id'],
                    producer_id=row['producent_id'],
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
                    # printsided=modify_printsided(row['printsided']),
                    # pressvarnish_front=modify_boleaninput(row['pressvarnish_front']),
                    # pressvarnish_rear=modify_boleaninput(row['pressvarnish_rear']),
                    pressvarnish_booklet=persvernis_bw,
                    # enhance_sided=modify_printsided(row['enhance_sided']),
                    # enhance_front=find_enhancement_id(row['enhance_front']),
                    # enhance_rear=find_enhancement_id(row['enhance_rear']),
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
                new_selfcover_printproject.save()

        print('drukwerkmaatwerk selfcover printprojects veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk selfcover printprojects veldhuis load: ', str(e))


def load_selfcover_offers_veldhuis(inputfolder, inputfile):
    try:
        with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
            selfcover_offers_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
                                                    encoding="utf-8")
            selfcover_offers_veldhuis_oud = Offers.objects.filter(producer_id=2, productcategory_id=3)
            selfcover_offers_veldhuis_oud.delete()

            # klant_id,producent_id,perc_korting_tw_brochures_gebonden,manager,user_admin,bedrijfsnaam,telefoonnummer_algemeen,e_mail_algemeen,straat_huisnummer,postcode,plaats,actief,is_welkom,perc_korting_tw_brochures_gehecht,perc_korting_tw_folders,perc_korting_tw_plano,perc_korting_tw_selfcovers,perc_korting_tw_sheets,created,
            # perc_korting_tw_enveloppen,eigen_offertetemplate,locatie_offertetemplate,perc_korting_tw_brochures_garenloos
            for index, row in selfcover_offers_veldhuis.iterrows():

                offerstatus = 2
                if row['aanvraag_status'] == 'Order':
                    offerstatus = 3

                persvernis_bw = 0
                if row['persvernis_bw'] == 'Ja':
                    persvernis_bw = 1

                new_selfcover_offer = Offers(
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
                new_selfcover_offer.save()

        print('drukwerkmaatwerk selfcover offers veldhuis loaded')
    except Exception as e:
        print('error drukwerkmaatwerk selfcover offers veldhuis load: ', str(e))


# def load_selfcover_calculations_veldhuis(inputfolder, inputfile):
#     try:
#         with open(inputfolder + inputfile, 'r') as printprojects_veldhuis_csv_file:
#             selfcover_printprojects_veldhuis = pd.read_csv(printprojects_veldhuis_csv_file, delimiter=',', header=0,
#                                                            encoding="utf-8")
#             selfcover_calculations_veldhuis_oud = Calculations.objects.filter(producer_id=2, productcategory_id=3,
#                                                                               assortiment_item=False)
#             selfcover_calculations_veldhuis_oud.delete()
#
#             for index, row in selfcover_printprojects_veldhuis.iterrows():
#
#                 aanvraag_status = 2
#                 if row['aanvraag_status'] == 'Order':
#                     aanvraag_status = 3
#
#                 persvernis_bw = 0
#                 if row['persvernis_bw'] == 'Ja':
#                     persvernis_bw = 1
#
#                 try:
#                     paperspec_id_booklet = PaperCatalog.objects.get(paperbrand=row['papiersoort_bw'],
#                                                                     papercolor=row['papierkleur_bw'],
#                                                                     paperweight_m2=row['papiergewicht_m2_bw']
#                                                                     )
#                 except PaperCatalog.DoesNotExist:
#                     paperspec_id_booklet = []
#
#
#
#                 new_selfcover_calculation = Calculations(
#                     status='calculated',
#                     member_id=row['klant_id'],
#                     error=None,
#                     # printer=row['printer'],
#                     printer_booklet=row['machinenaam'],
#                     # printer_cover=row['printer_cover'],
#
#                     # cuttingmachine=row['cuttingmachine'],
#                     cuttingmachine_booklet=row['snijmachine_bw'],
#
#                     foldingmachine=row['vouwmachine_id'],
#                     foldingmachines_booklet=row['foldingmachines_booklet'],
#                     bindingmachine=row['brocheermachine'],
#
#                     # paperspec_id=row['paperspec_id'],
#                     paperspec_id_booklet=paperspec_id_booklet,
#                     # paperspec_id_cover=row['paperspec_id_cover'],
#                     purchase_paper_perc_added=0,
#
#                     pages_per_sheet_booklet=row['paginas_per_drukvel_bw'],
#                     pages_per_katern_booklet=row['paginas_per_vouwvel_bw'],
#                     number_of_printruns_booklet=row['aantal_drukstarts_bw'],
#                     # book_thickness=0 # row['book_thickness'],
#
#                     waste_printing=row['inschiet_drukken_bw'],
#                     waste_printing1000extra=row['inschiet_drukken_1000meer_bw'],
#                     waste_folding=row['inschiet_vouwen'],
#                     waste_folding1000extra=row['inschiet_vouwen_1000meer'],
#                     waste_binding=row['brocheren_inschiet'],
#                     waste_binding1000extra=row['brocheren_inschiet_1000meer'],
#                     # waste_printing_cover=row['waste_printing_cover'],
#                     # waste_printing_cover1000extra=row['waste_printing_cover1000extra'],
#                     # waste_binding_cover=row['waste_binding_cover'],
#                     # waste_binding_cover1000extra=row['waste_binding_cover1000extra'],
#
#                     order_startcost=row['startkosten'],
#                     printingcost=row['productiekosten_drukken'],
#                     printingcost_booklet=row['printingcost_booklet'],
#                     printingcost_cover=row['printingcost_cover'],
#                     printingcost1000extra=row['printingcost1000extra'],
#                     printingcost_booklet1000extra=row['printingcost_booklet1000extra'],
#                     printingcost_cover1000extra=row['printingcost_cover1000extra'],
#
#                     inkcost=row['inktkosten'],
#                     inkcost1000extra=row['inktkosten_1000meer'],
#                     # inkcost_cover=0, # row['inkcost_cover'],
#                     # inkcost_cover1000extra=0, # row['inkcost_cover1000extra'],
#                     # inkcost_booklet=0 # row['inkcost_booklet'],
#                     # inkcost_booklet1000extra=0 # row['inkcost_booklet1000extra'],
#
#                     foldingcost=row['vouwen_bw'],
#                     foldingcost1000extra=row['vouwen_1000meer'],
#                     foldingcost_booklet=row['vouwen_bw'],
#                     foldingcost_booklet1000extra=row['vouwen_1000meer'],
#
#                     bindingcost=row['bindingcost'],
#                     bindingcost1000extra=row['bindingcost1000extra'],
#
#                     # enhancecost=row['enhancecost'],
#                     # enhancecost1000extra=row['enhancecost1000extra'],
#                     # enhancecost_cover=row['enhancecost_cover'],
#                     # enhancecost_cover1000extra=row['enhancecost_cover1000extra'],
#
#                     purchase_plates=row['inkoop_platen_bw'],
#                     margin_plates=row['tw_platen_bw'],
#                     # platecost= row['inkoop_platen_bw']+row['tw_platen_bw'],
#                     purchase_plates_booklet=row['inkoop_platen_bw'],
#                     margin_plates_booklet=row['tw_platen_bw'],
#                     # platecost_booklet=row['platecost_booklet'],
#                     # purchase_plates_cover=row['purchase_plates_cover'],
#                     # margin_plates_cover=row['margin_plates_cover'],
#                     # platecost_cover=row['platecost_cover'],
#
#                     papercost_total=row['papercost_total'],
#                     papercost_total1000extra=row['papercost_total1000extra'],
#                     papercost_booklet_total=row['papercost_booklet_total'],
#                     papercost_booklet_total1000extra=row['papercost_booklet_total1000extra'],
#                     papercost_cover_total=row['papercost_cover_total'],
#                     papercost_cover_total1000extra=row['papercost_cover_total1000extra'],
#
#                     net_paper_quantity=row['net_paper_quantity'],
#                     net_paper_quantity1000extra=row['net_paper_quantity1000extra'],
#                     net_paper_quantity_booklet=row['net_paper_quantity_booklet'],
#                     net_paper_quantity_booklet1000extra=row['net_paper_quantity_booklet1000extra'],
#                     net_paper_quantity_cover=row['net_paper_quantity_cover'],
#                     net_paper_quantity_cover1000extra=row['net_paper_quantity_cover1000extra'],
#
#                     paper_quantity=row['inkoop_papier_bw'],
#                     # paper_quantity1000extra=row['paper_quantity1000extra'],
#                     paper_quantity_booklet=row['inkoop_papier_bw'],
#                     # paper_quantity_booklet1000extra=row['paper_quantity_booklet1000extra'],
#                     # paper_quantity_cover=row['paper_quantity_cover'],
#                     # paper_quantity_cover1000extra=row['paper_quantity_cover1000extra'],
#                     #
#                     # number_of_printruns_cover=row['number_of_printruns_cover'],
#
#                     packagingcost=row['packagingcost'],
#                     packagingcost1000extra=row['packagingcost1000extra'],
#
#                     orderweight_kg=row['orderweight_kg'],
#                     orderweight_kg1000extra=row['orderweight_kg1000extra'],
#                     transportcost=row['transportcost'],
#                     transportcost1000extra=row['transportcost1000extra'],
#
#                     cuttingcost=row['cuttingcost'],
#                     cuttingcost1000extra=row['cuttingcost1000extra'],
#                     cuttingcost_booklet=row['cuttingcost_booklet'],
#                     cuttingcost_booklet1000extra=row['cuttingcost_booklet1000extra'],
#                     cuttingcost_cover=row['cuttingcost_cover'],
#                     cuttingcost_cover1000extra=row['cuttingcost_cover1000extra'],
#
#
#                     transportationcost=row['transportcost'],
#                     transportationcost1000extra=row['transportcost1000extra'],
#
#                     total_cost=row['total_cost'],
#                     total_cost1000extra=row['total_cost1000extra'],
#                     added_value=row['added_value'],
#                     perc_added_value=row['perc_added_value'],
#                     added_value1000extra=row['added_value1000extra'],
#                     perc_added_value1000extra=row['perc_added_value1000extra'],
#                     memberdiscount=row['memberdiscount'],
#                     memberdiscount1000extra=row['memberdiscount1000extra'],
#                     offer_date=timezone.now().today().date(),
#                     offer_value=row['offer_value'],
#                     offer_value1000extra=row['offer_value1000extra'],
#
#                 )
#                 new_selfcover_calculation.save()
#
#         print('drukwerkmaatwerk selfcover calculations veldhuis loaded')
#     except Exception as e:
#         print('error drukwerkmaatwerk selfcover calculations veldhuis load: ', str(e))
