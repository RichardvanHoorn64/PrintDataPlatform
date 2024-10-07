from offers.models import *
from orders.models import OrderStatus


def excel_fill_worksheet(worksheet, df, columns, bold):
    # Fill first row with header in bold
    row = 0
    for i, elem in enumerate(columns):
        worksheet.write(row, i, elem, bold)
    row += 1
    # Now fill other rows with columns
    index = 0
    while index < len(df):
        for i, elem in enumerate(columns):
            try:
                fieldvalue = df.iloc[index][elem]
                if isinstance(fieldvalue, (list, tuple)):
                    return str(fieldvalue)[1:-1]
            except KeyError:
                fieldvalue = []

            try:
                worksheet.write(row, i, fieldvalue)
            except Exception as e:
                print("no value written for: ", elem, e)
        index = index + 1
        row += 1


def retrieve_productcategory(productcategory_id):
    try:
        productcategoryname = ProductCategory.objects.get(productcategory_id=productcategory_id).productcategory
    except ValueError:
        productcategoryname = ""
    return productcategoryname


def retrieve_client(client_id, member_id):
    if client_id:
        try:
            clientname = Clients.objects.get(client_id=client_id, member_id=member_id).client
        except ValueError:
            clientname = ""

    else:
        clientname = ""
    return clientname


def retrieve_company(member_id):
    if member_id:
        try:
            company = Members.objects.get(member_id=member_id).company
        except ValueError:
            company = ""
    else:
        company = ""
    return company


def retrieve_projectmanager(user_id):
    try:
        user = UserProfile.objects.get(id=user_id)
        projectmanagername = user.first_name + " " + user.last_name
    except ValueError:
        projectmanagername = ""

    return projectmanagername


def retrieve_orderer(orderer_id):
    if orderer_id:
        try:
            orderer = UserProfile.objects.get(id=orderer_id)
            orderername = orderer.first_name + " " + orderer.last_name
        except ValueError:
            orderername = ""
    else:
        orderername = ""
    return orderername


def retrieve_clientcontact(clientcontact_id, member_id):
    if clientcontact_id:
        try:
            clientcontactname: str = ClientContacts.objects.get(clientcontact_id=clientcontact_id,
                                                                member_id=member_id).clientcontact
        except ValueError:
            clientcontactname = ""
    else:
        clientcontactname = ""

    return clientcontactname


def retrieve_producer(producer_id):
    try:
        producername = Producers.objects.get(producer_id=producer_id).company
    except ValueError:
        producername = ""
    return producername


def retrieve_project_title(printproject_id):
    try:
        printprojectname = PrintProjects.objects.get(printproject_id=printproject_id).project_title
    except ValueError:
        printprojectname = ""
    return printprojectname


def retrieve_printprojectstatus(printprojectstatus_id):
    try:
        printprojectstatusname = PrintprojectStatus.objects.get(
            printprojectstatus_id=printprojectstatus_id).printprojectstatus
    except ValueError:
        printprojectstatusname = ""
    return printprojectstatusname


def retrieve_offerstatus(offerstatus_id):
    try:
        offerstatusname = Offerstatus.objects.get(offerstatus_id=offerstatus_id).offerstatus
    except ValueError:
        offerstatusname = ""
    return offerstatusname


def retrieve_orderstatus(orderstatus_id):
    try:
        orderstatusname = OrderStatus.objects.get(orderstatus_id=orderstatus_id).orderstatus
    except ValueError:
        orderstatusname = ""
    return orderstatusname
