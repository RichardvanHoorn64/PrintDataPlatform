from index.categories_groups import *
from index.models import BrandPortalData
from printprojects.models import MemberProducerMatch
from profileuseraccount.models import Members


def define_exclusive_producer_id(user):
    member_plan_id = user.member_plan_id
    exclusive_producer_id = 1

    if member_plan_id in producer_memberplans:
        exclusive_producer_id = user.producer.producer_id

    if member_plan_id in exclusive_memberplans:
        exclusive_producer_id = user.member.exclusive_producer_id

    return exclusive_producer_id


def define_site_name(user):
    if user.is_anonymous:
        site_name = 'PrintDataPlatform'
    elif user.member_plan_id in exclusive_memberplans:
        site_name = str(user.producer.company)
    elif user.member_plan_id in producer_memberplans:
        site_name = 'PrintDataPlatform ' + str(user.producer.company)
    else:
        site_name = 'PrintDataPlatform'
    return site_name


def img_loc_logo(user):
    if user.is_anonymous:
        img_loc_logo_static = "assets/img/logos/header_1.jpg"
    elif user.member_plan_id in exclusive_memberplans:
        producer_id = user.producer.producer_id
        img_loc_logo_static = "assets/img/logos/header_" + str(producer_id) + ".jpg"
    else:
        img_loc_logo_static = "assets/img/logos/header_1.jpg"
    return img_loc_logo_static

def define_exclusive_site_name(user):
    member_plan_id = user.member_plan_id
    exclusive_site_name = define_site_name(user)

    if member_plan_id in exclusive_memberplans:
        exclusive_site_name = BrandPortalData.objects.get(producer_id=define_exclusive_producer_id(user)).brandportal
    return exclusive_site_name


def update_exclusive_members(user):
    producer_id = user.producer_id
    member_matchlist = MemberProducerMatch.objects.filter(producer_id=producer_id).values_list('member_id', flat=True)
    exclusive_members = Members.objects.filter(exclusive_producer=producer_id)

    for exclusive_member in exclusive_members:
        try:
            if exclusive_member.member_id not in member_matchlist:
                new_match = MemberProducerMatch.objects.create(
                    producer_id=producer_id,
                    member_id=exclusive_member.member_id)
                new_match.save()
        except Exception as e:
            print('update exclusive members error: ', exclusive_member, e)
