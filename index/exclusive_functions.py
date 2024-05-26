from index.categories_groups import *


def define_exclusive_producer_id(user):
    member_plan_id = user.member_plan_id
    exclusive_producer_id = 1

    if member_plan_id in producer_memberplans:
        exclusive_producer_id = user.producer.producer_id

    if member_plan_id in exclusive_memberplans:
        exclusive_producer_id = user.member.exclusive_producer_id

    return exclusive_producer_id
