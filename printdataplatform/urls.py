from api.views import *
from django.contrib import admin
from django.urls import path, include
from assets.asset_views import *
from assets.asset_deleteviews import *
from calculations.assortiment_views import *
from downloads.download_paperspecs import *
from downloads.download_producer_offer_doc import *
from downloads.member_downloads import *
from downloads.producer_downloads import *
# from downloads.download_client_docs import *
from index.dashboard_views import *
from index.drukwerkmaatwerk_etl import LoadVeldhuisDataView
from index.index_views import *
from index.note_views import *
from index.json_views import *
from materials.material_views import *
from materials.paper_upload_view import UploadProducerPaperCatalog
from materials.paper_views import *
from materials.views_json import *
from members.account_views import *
from members.client_views import *
from members.crm_functions import *
from members.crm_views import *
from offers.offer_functions import *
from offers.offer_views import *
from orders.order_views import *
from printprojects.clone_printproject_view import *
from printprojects.detail_views import *
from printprojects.start_printproject_view import *
from printprojects.start_workflow_view import PrintProjectStartWorkflowView, SendRFQView, ChangePrintProjectMatch
from producers.contact_views import *
from producers.offer_views import *
from producers.producer_views import *
from producers.tariff_views import *
from profileuseraccount.accountviews.CreateUserProfileView import *
from profileuseraccount.accountviews.RegistrationViews import *

# printdata URL Configuration
urlpatterns = [
    # (r'^i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    # open homepages, no inlog required
    path('', WelcomeView.as_view(), name=''),  # redirect page
    path('welcome/', WelcomeView.as_view(), name='welcome'),  # redirect page

    path('load_veldhuis_data/', LoadVeldhuisDataView.as_view(), name='load_veldhuis_data'),

    path('home/', WelcomeView.as_view(), name='home'),
    path('signup/', UserProfileCreateView.as_view(), name='signup'),
    path('signup_landing/', SignupLandingView.as_view(), name='signup_landing'),
    path('no_access/', NoAccessView.as_view(), name='no_access'),
    path('wait_for_approval/', WaitForApproval.as_view(), name='wait_for_approval'),

    # dashboards after member accept and inlog
    path('printdataplatform_dashboard/', PrintDataPlatformDashboard.as_view(),
         name='printdataplatform_dashboard'),

    path('printproject_dashboard/<int:printprojectstatus_id>', PrintprojectDashboard.as_view(),
         name='printproject_dashboard'),

    # printdataplatform
    path('conditions/', ConditionView.as_view(), name='conditions'),
    path('faq/', FaqView.as_view(), name='faq'),
    path('conditions/', ConditionView.as_view(), name='conditions'),
    path('events/', EventsView.as_view(), name='events'),

    # printprojects
    path('change_printproject_match/<int:printprojectmatch_id>', ChangePrintProjectMatch.as_view(),
         name='change_printproject_match'),

    path('new_printproject/<int:productcategory_id>', CreateNewPrintProjectView.as_view(), name='new_printproject'),

    path('start_printproject_workflow/<int:printproject_id>', PrintProjectStartWorkflowView.as_view(),
         name='start_printproject_workflow'),

    # update pricing
    path('printproject_details/<int:printproject_id>', PrintProjectDetailsView.as_view(),
         name='printproject_details'),
    # update pricing
    path('printproject_clone/<int:printproject_id>', PrintProjectCloneView.as_view(),
         name='printproject_clone'),
    path('printproject_update/<int:printproject_id>', PrintProjectCloneUpdateView.as_view(),
         name='printproject_update'),

    path('printproject_delete/<int:printproject_id>', PrintProjectDeleteView.as_view(),
         name='printproject_delete'),

    # offers
    path('offer_dashboard/<int:offerstatus_id>', OfferDashboard.as_view(),
         name='offer_dashboard'),
    path('offer_details/<int:pk>', OfferDetailsMembersView.as_view(),
         name='offer_details'),
    path('offer_members_update/<int:pk>', OfferMembersUpdate.as_view(),
         name='offer_members_update'),

    path('offer_producers_form/<int:pk>', OfferProducersFormCheckView.as_view(),
         name='offer_producers_form'),
    path('offer_producers_update/<int:pk>', OfferProducersUpdate.as_view(),
         name='offer_producers_update'),
    path('offer_producers_update_form/<int:pk>/<int:reference_key>', OfferProducersOpenUpdate.as_view(),
         name='offer_producers_update_form'),


    path('deny_offer/<int:pk>', DenyOfferView.as_view(), name='deny_offer'),
    path('close_offer/<int:pk>/', CloseOfferView.as_view(), name='close_offer'),

    path('close_calculation_error/<int:pk>/', CloseErrorCalculationView.as_view(), name='close_calculation_error'),
    path('handle_offer/<int:offer_id>/<int:offerstatus_id>', HandleOfferView.as_view(),
         name='handle_offer'),

    path('thanks_submit_offer/', ThanksSubmitOffer.as_view(), name='thanks_submit_offer'),

    path('pricing_dashboard/<int:memberproducermatch_id>/', ProducerPricingUpdateView.as_view(),
         name='pricing_dashboard'),

    # orders
    path('order_dashboard/<int:order_status_id>', OrderDashboard.as_view(), name='order_dashboard'),
    path('create_order/<int:offer_id>', CreateOrderView.as_view(), name='create_order'),
    path('order_details/<int:order_id>', OrderDetailsView.as_view(), name='order_details'),
    path('order_delete/<int:order_id>', OrderDeleteView.as_view(), name='order_delete'),
    path('change_orderstatus/<int:order_id>/<int:order_status_id>',
         ChangeOrderStatus.as_view(), name='change_orderstatus'),

    # account
    path('my_account/<int:pk>', MyAccountView.as_view(), name='my_account'),
    path('my_account_update/<int:pk>', MyAccountUpdateView.as_view(), name='my_account_update'),
    path('business_account_update/<int:pk>', BusinessAccountUpdateView.as_view(), name='business_account_update'),
    path('my_account_delete/<int:pk>', MyAccountDeleteView.as_view(), name='my_account_delete'),
    path('create_co_worker/<int:member_id>', CoWorkerUserProfileCreateView.as_view(),
         name='create_co_worker'),
    # path('update_co_worker/<int:id>', CoWorkerUserProfileUpdateView.as_view(),
    # name='update_co_worker'),
    path('activate_co_worker/<int:id>', ActivateCoWorker.as_view(), name='activate_co_worker'),
    path('memberplan_up_downgrade/<int:member_id>', MemberplanUpDowngradeView.as_view(), name='memberplan_up_downgrade'),

    # clients
    path('client_dashboard/', ClientDashboard.as_view(), name='client_dashboard'),
    path('client_details/<int:pk>', ClientDetails.as_view(), name='client_details'),
    path('create_client/', CreateNewClient.as_view(), name='create_client'),
    path('create_clientcontact/<int:client_id>', CreateNewClientContact.as_view(),
         name='create_clientcontact'),
    path('update_client/<int:pk>', UpdateClient.as_view(), name='update_client'),
    path('update_clientcontact/<int:pk>', UpdateClientContact.as_view(),
         name='update_clientcontact'),
    path('delete_client/<int:client_id>', DeleteClient.as_view(), name='delete_client'),
    path('delete_clientcontact/<int:pk>', DeleteClientContact.as_view(),
         name='delete_clientcontact'),

    # producers
    path('my_suppliers/', MySuppliers.as_view(), name='my_suppliers'),

    path('create_new_producer/', CreateNewProducer.as_view(), name='create_new_producer'),
    path('producer_details/<int:pk>/', ProducerDetails.as_view(), name='producer_details'),
    path('change_memberproducerstatus/<int:memberproducermatch_id>/<int:memberproducerstatus_id>',
         ChangeMemberProducerStatus.as_view(), name='change_memberproducerstatus'),

    # producer contacts
    path('create_producercontact/<int:producer_id>', CreateNewProducerContact.as_view(),
         name='create_producercontact'),

    path('update_producercontact/<int:producercontact_id>', UpdateProducerContact.as_view(),
         name='update_producercontact'),
    path('delete_producercontact/<int:producercontact_id>', DeleteProducerContact.as_view(),
         name='delete_producercontact'),

    path('update_producercommunication/<int:producer_id>', UpdateProducerCommunication.as_view(),
         name='update_producercommunication'),

    path('producer_close_order//<int:pk>', ProducerCloseOrderView.as_view(), name='producer_close_order'),
    path('producer_accept_order//<int:pk>', ProducerAcceptOrderView.as_view(), name='producer_accept_order'),

    # producer sales dashboard
    path('producer_sales_dashboard/<int:offerstatus_id>', ProducerSalesDashboard.as_view(),
         name='producer_sales_dashboard'),

    # producer offers
    path('producer_offers/<int:offerstatus_id>', ProducerOffers.as_view(), name='producer_offers'),
    path('producer_offer_details/<int:offer_id>', ProducerOfferDetails.as_view(), name='producer_offer_details'),
    path('producer_error_details/<int:calculation_id>', ProducerErrorDetails.as_view(), name='producer_error_details'),
    path('select_supplier_productoffering_switch/<str:setting_id>', ProducerProductofferingSwitch.as_view(),
         name='select_supplier_productoffering_switch'),
    path('producer_calculation_errors/', ProducerCalculationErrors.as_view(), name='producer_calculation_errors'),

    # producers member dashboard
    path('producer_open_members/', ProducerOpenMembers.as_view(), name='producer_open_members'),

    path('member_details/<int:pk>/', ProducerMemberDetails.as_view(), name='member_details'),
    path('producer_memberaccept/<int:pk>', ProducerMemberAccept.as_view(), name='producer_memberaccept'),
    path('producer_member_autoquote/<int:pk>', ProducerMemberAutoQuote.as_view(), name='producer_member_autoquote'),

    # producer orders
    path('producer_orders/<int:order_status_id>', ProducerOrders.as_view(), name='producer_orders'),

    # rfq workflow
    path('select_clientcontact_json/<int:client_id>', select_clientcontact_json,
         name='select_clientcontact_json'),
    path('select_supplier_switch_json/<str:printprojectmatch_id>', select_supplier_switch_json,
         name='select_supplier_switch_json'),
    path('send_rfq/<int:printproject_id>', SendRFQView.as_view(), name='send_rfq'),
    path('offer_acceskey_submit/<int:offer_id>/<int:offer_key_test>/', offer_acceskey_submit,
         name='offer_acceskey_submit'),

    path('paper_catalog/', ProducerPaperCatalog.as_view(), name='paper_catalog'),
    path('producer_paper_catalog_download/', DownloadProducerPaperCatalog.as_view(),
         name='producer_paper_catalog_download'),
    path('producer_paper_catalog_upload/', UploadProducerPaperCatalog.as_view(), name='producer_paper_catalog_upload'),

    # paper
    path('paper_brands/<str:papercategory>', PaperBrandsDisplay.as_view(), name='paper_brands'),
    path('download_paperbrands', DownloadPaperBrands.as_view(), name='download_paperbrands'),

    # java / ajax urls paperchoices for quotes paperselection
    path('paperbrand_json/<str:papercategory>', get_json_paperbrand, name='paperbrand_json'),
    path('paperweight_json/<str:paperbrand>', get_json_paperweight,
         name='paperweight_json'),
    path('papercolor_json/<str:paperbrand>/<int:paperweight>', get_json_papercolor, name='papercolor_json'),

    # path('papercategory_cover_json', get_json_cover_papercategory, name='papercategory_cover_json'),
    path('paperbrand_cover_json/<str:papercategory>', get_json_cover_paperbrand,
         name='paperbrand_cover_json'),
    path('paperweight_cover_json/<str:paperbrand>', get_json_cover_paperweight,
         name='paperweight_cover_json'),
    path('papercolor_cover_json/<str:paperbrand>/<int:paperweight>', get_json_cover_papercolor,
         name='papercolor_cover_json'),

    # java / ajax urls paperchoices for quotes calculate folder number of pages
    path('folder_number_of_pages_json/<str:foldingmethod_id>', get_json_folder_number_of_pages,
         name='folder_number_of_pages_json'),

    # create notes
    path('delete_note/<int:note_id>', DeleteNoteView.as_view(), name='delete_note'),

    # api's
    # path('producer_api_manager/<int:pk>', APIproducerManager.as_view(), name='producer_api_manager'),
    # path('api_producer_accept/<int:pk>', APIproducerAccept.as_view(), name='api_producer_accept'),

    # downloads
    path('member_download_printprojects/', MemberDownloadPrintprojects.as_view(),
         name='member_download_printprojects'),
    path('member_download_clients/', MemberDownloadClients.as_view(),
         name='member_download_clients'),

    path('producer_download_offer/<int:offer_id>', DownloadProducerOffer.as_view(),
         name='producer_download_offer'),  # doc_id 1= offer, 2 =invoice

    path('producer_download_offers/', ProducerDownloadOffers.as_view(),
         name='producer_download_offers'),

    path('producer_download_orders/', ProducerDownloadOrders.as_view(),
         name='producer_download_orders'),

    # Assets producers
    path('asset_dashboard/', AssetDashboardView.as_view(), name='asset_dashboard'),
    path('create_printer/', CreatePrinter.as_view(), name='create_printer'),
    path('update_printer/<int:printer_id>', UpdatePrinter.as_view(), name='update_printer'),

    path('create_foldingmachine/<int:foldingtype_id>', CreateFoldingmachine.as_view(), name='create_foldingmachine'),
    path('update_foldingmachine/<int:foldingmachine_id>', UpdateFoldingmachine.as_view(), name='update_foldingmachine'),

    path('create_cuttingmachine/', CreateCuttingmachine.as_view(), name='create_cuttingmachine'),
    path('update_cuttingmachine/<int:cuttingmachine_id>', UpdateCuttingmachine.as_view(), name='update_cuttingmachine'),

    path('create_bindingmachine/', CreateBindingmachine.as_view(), name='create_bindingmachine'),
    path('update_bindingmachine/<int:bindingmachine_id>', UpdateBindingmachine.as_view(), name='update_bindingmachine'),

    # Tariff and settings producers
    path('producer_tariffs/', ProducerTariffs.as_view(), name='producer_tariffs'),
    path('producer_tariffs_update/<int:settings_id>', ProducerTariffsUpdate.as_view(), name='producer_tariffs_update'),
    path('enhancement_create/', ProducerEnhancementCreate.as_view(),
         name='enhancement_create'),
    path('change_enhancement_added_value/<int:enhancementtariff_id>', ChangeEnhancementAddedValue.as_view(),
         name='change_enhancement_added_value'),
    path('change_transport_added_value/<int:transporttariff_id>', ChangeTransportAddedValue.as_view(),
         name='change_transport_added_value'),

    path('enhancement_update/<int:enhancementtariff_id>', ProducerEnhancementUpdate.as_view(),
         name='enhancement_update'),
    path('enhancement_delete/<int:enhancementtariff_id>', ProducerEnhancementDelete.as_view(),
         name='enhancement_delete'),
    path('packaging_update/<int:packagingtariff_id>', ProducerPackagingUpdate.as_view(), name='packaging_update'),
    path('transport_update/<int:transporttariff_id>', ProducerTransportUpdate.as_view(), name='transport_update'),

    path('change_pms_availability/<int:setting_id>', ChangePMSAvailability.as_view(), name='change_pms_availability'),

    # change tariff availability
    path('change_enhancement_availability/<int:enhancementtariff_id>', ChangeEnhancementAvailability.as_view(),
         name='change_enhancement_availability'),
    path('change_packaging_availability/<int:packagingtariff_id>', ChangePackagingAvailability.as_view(),
         name='change_packaging_availability'),
    path('change_transport_availability/<int:transporttariff_id>', ChangeTransportAvailability.as_view(),
         name='change_transport_availability'),

    # delete production assets
    path('delete_printer/<int:pk>', PrinterDelete.as_view(), name='delete_printer'),
    path('delete_cuttingmachine/<int:pk>', CuttingmachineDelete.as_view(), name='delete_cuttingmachine'),
    path('delete_foldingmachine/<int:pk>', FoldingmachineDelete.as_view(), name='delete_foldingmachine'),
    path('delete_bindingmachine/<int:pk>', BindingmachineDelete.as_view(),
         name='delete_bindingmachine'),

    # Producer assortiment view, upload and download
    path('producer_assortiment/', AssortimentView.as_view(), name='producer_assortiment'),
    path('producer_assortiment_upload/<str:error>', UploadAssortimentCSV.as_view(), name='producer_assortiment_upload'),
    path('producer_assortiment_calculate/', CalculateAssortiment.as_view(), name='producer_assortiment_calculate'),
    path('producer_assortiment_download/', DownloadAssortiment.as_view(), name='producer_assortiment_download'),
    path('producer_calculationdetails/<int:calculation_id>', ProducerCalculationDetails.as_view(),
         name='producer_calculationdetails'),

    path('error_test/', TestErrorView.as_view(), name='error_test'),

]
