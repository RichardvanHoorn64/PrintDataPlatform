from assets.models import *
from producers.models import EnhancementTariffs


def define_productofferlist(user):
    try:
        producer_id = user.producer_id
        productofferlist = GeneralCalculationSettings.objects.get(producer_id=producer_id)
    except:
        productofferlist = []

    return productofferlist


def enhancement_update(producer_id):
    from index.product_choices import enhance_choices
    producer_id = producer_id
    enhancement_dictlist_pr = list(EnhancementTariffs.objects.filter(producer_id=producer_id).values('type'))
    enhancement_actief = [enhancement['type'] for enhancement in enhancement_dictlist_pr]
    verschil = [x for x in enhance_choices if not x in enhancement_actief]

    for enhancement in verschil:
        producer_id = producer_id
        new_enhancement_dict = {
            'producer_id': producer_id,
            'type': enhancement,
            'availeble': False,
        }

        new_enhancement = EnhancementTariffs(**new_enhancement_dict)
        new_enhancement.save()
