from index.categories_groups import *

def define_site_name(user):
    if user.is_anonymous:
        site_name = 'PrintDataPlatform'
    elif user.member_plan_id in producer_memberplans:
        site_name = 'PrintDataPlatform ' + str(user.producer.company)
    else:
        site_name = 'PrintDataPlatform'
    return site_name


def img_loc_logo(user):
    if user.is_anonymous:
        img_loc_logo_static = "assets/img/logos/header_1.jpg"
    else:
        img_loc_logo_static = "assets/img/logos/header_1.jpg"
    return img_loc_logo_static

