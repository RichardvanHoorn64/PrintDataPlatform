from index.categories_groups import *
from index.models import BrandPortalData


def define_exclusive_producer_id(user):
    member_plan_id = user.member_plan_id
    exclusive_producer_id = 1

    if member_plan_id in producer_memberplans:
        exclusive_producer_id = user.producer.producer_id

    if member_plan_id in exclusive_memberplans:
        exclusive_producer_id = user.member.exclusive_producer_id

    return exclusive_producer_id


def define_exclusive_site_name(user):
    member_plan_id = user.member_plan_id
    exclusive_site_name = site_name

    if member_plan_id in exclusive_memberplans:
        exclusive_site_name = BrandPortalData.objects.get(producer_id=define_exclusive_producer_id(user)).brandportal
    return exclusive_site_name
