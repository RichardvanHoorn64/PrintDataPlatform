from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from index.display_functions import *
from index.models import ProductCategory
from offers.models import Offers
from printprojects.models import PrintProjects
from profileuseraccount.form_invalids import error_mail_admin
from printdataplatform.settings import EMAIL_HOST_USER
from orders.models import Orders
from profileuseraccount.models import *
from index.categories_groups import *


# send orderdetails to producer
def send_ordermail_producer(order_id):
    order = Orders.objects.get(order_id=order_id)

    # offer
    offer_id = order.offer_id
    offer = Offers.objects.get(offer_id=offer_id)

    # printproject
    printproject_id = order.printproject_id
    printproject = PrintProjects.objects.get(printproject_id=printproject_id)
    productcategory_id = printproject.productcategory_id

    # producer
    producer = Producers.objects.get(producer_id=order.producer_id)

    # buyer
    printorder_requester = order_requester(order)
    member = Members.objects.get(member_id=order.member_id)

    # order details
    productcategory = ProductCategory.objects.get(productcategory_id=productcategory_id).productcategory
    description = printproject_description(printproject, productcategory)
    own_quotenumber = printproject_own_quotenumber(printproject)

    printproject = printproject
    order_size = printproject_size(printproject)

    # order descriptions
    paper = printproject_paper(printproject.papercategory, printproject.paperbrand,
                               printproject.paperweight, printproject.papercolor)
    printing_booklet = printproject_printing_booklet(
        printproject.print_booklet,
        printproject.number_pms_colors_booklet,
        printproject.pressvarnish_booklet)

    printing_cover = printproject_printing(printproject.printsided, printproject.print_front,
                                           printproject.print_rear,
                                           printproject.number_pms_colors_front,
                                           printproject.number_pms_colors_rear)

    paper_cover = printproject_paper(printproject.papercategory_cover,
                                     printproject.paperbrand_cover,
                                     printproject.paperweight_cover,
                                     printproject.papercolor_cover)
    printing = printproject_printing(printproject.printsided, printproject.print_front,
                                     printproject.print_rear,
                                     printproject.number_pms_colors_front,
                                     printproject.number_pms_colors_rear)
    varnish = printproject_varnish(printproject.printsided, printproject.pressvarnish_front,
                                   printproject.pressvarnish_rear)
    enhance = printproject_enhance(printproject.productcategory_id,
                                   printproject.enhance_sided, printproject.enhance_front,
                                   printproject.enhance_rear, )
    finishing = printproject_finishing(printproject)

    packaging = printproject_packaging(printproject.packaging)

    message_extra_work = printproject_message_extra_work(printproject.message_extra_work)

    salesprice = printproject_salesprice(printproject)
    salesprice1000extra = printproject_salesprice1000extra(printproject)
    offer_table_title = "Aanbiedingen voor: " + description

    nmber_of_pages = printproject_number_of_pages(printproject)


    merge_data = {
        'producer' : producer,
        'offer': offer,
        'offer_date' : offer.offer_date.date(),
        'order': order,
        'own_quotenumber': own_quotenumber,
        'productcategory_id' : productcategory_id,
        'printproject': printproject,
        'member': member,
        'order_size': order_size,

        'requester': printorder_requester,
        'description': description,
        'size': printproject_size,

        'paper': paper,
        'paper_cover': paper_cover,

        'printing': printing,
        'printing_booklet': printing_booklet,
        'printing_cover': printing_cover,

        'status': str(order.order_status),

        'varnish': varnish,
        'enhance': enhance,
        'finishing': finishing,
        'packaging': packaging,
        'message_extra_work': message_extra_work,
        'salesprice': salesprice,
        'salesprice1000extra': salesprice1000extra,

        'offer_table_title': offer_table_title,
        'nmber_of_pages': nmber_of_pages,
        'delivery_adress': order_delivery_adress(order),
        'delivery_contact' : order_delivery_contact(order),

        'categories_plano' : categories_plano,
        'categories_folders' : categories_folders,
        'categories_selfcovers' : categories_selfcovers,
        'categories_brochures_all' : categories_brochures_all,
        'categories_brochures_cover' : categories_brochures_cover,
    }

    # send ordermail
    try:
        email_template = 'orders/ordermail_includes/email_order_notice.html'
        subject = render_to_string("orders/ordermail_includes/order_notice_subject.txt", merge_data)
        html_body = render_to_string(email_template, merge_data)
        adress = recepients = producer.e_mail_orders
        send_printdataplatform_mail(subject, address, html_body)
    except Exception as e:
        error_mail_admin('order_mail.send() error: ', e)

