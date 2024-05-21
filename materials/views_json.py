from django.http import JsonResponse

from index.exclusive_functions import define_exclusive_producer_id
from materials.models import *


# dropdown paperbrand
def get_json_paperbrand(request, **kwargs):
    user = request.user
    exclusive_producer_id = define_exclusive_producer_id(user)
    papercategory_id = kwargs.get('papercategory_id')
    papercategory = PaperCategories.objects.get(papercategory_id=papercategory_id, producer_id=exclusive_producer_id).papercategory
    paperbrands = list(PaperBrands.objects.filter(papercategory=papercategory, producer_id=exclusive_producer_id).values().order_by('paperbrand'))
    return JsonResponse({'data': paperbrands})


# dro pdown paperweight
def get_json_paperweight(request, **kwargs):
    paperbrand_id = kwargs.get('paperbrand_id')
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    paperbrand = PaperBrands.objects.get(paperbrand_id=paperbrand_id).paperbrand
    paperweights = list(
        PaperWeights.objects.filter(paperbrand=paperbrand, producer_id=exclusive_producer_id).values().order_by(
            'paperweight_m2'))
    return JsonResponse({'data': paperweights})


# dropdown papercolor
def get_json_papercolor(request, **kwargs):
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    paperweight_id = kwargs.get('paperweight_id')
    paperweight_data = PaperWeights.objects.get(paperweight_id=paperweight_id)
    paperweight_m2 = paperweight_data.paperweight_m2
    paperbrand = paperweight_data.paperbrand
    papercolors = list(PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight_m2).values())
    return JsonResponse({'data': papercolors})


# For brochures covers

# dropdown papercategory cover
def get_json_cover_papercategory(request, **kwargs):
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    papercategories_cover = list(PaperCategories.objects.filter(brochures_cover=True).values().order_by('papercategory'))
    return JsonResponse({'data': papercategories_cover})


# dropdown paperweight fill cover
def get_json_cover_paperbrand(request, **kwargs):
    papercategory_id = kwargs.get('papercategory_id')
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    papercategory = PaperCategories.objects.get(papercategory_id=papercategory_id).papercategory
    paperbrands_cover = list(PaperBrands.objects.filter(papercategory=papercategory).values().order_by('paperbrand'))
    return JsonResponse({'data': paperbrands_cover})


def get_json_cover_paperweight(request, **kwargs):
    paperbrand_id = kwargs.get('paperbrand_id')
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    paperbrand = PaperBrands.objects.get(paperbrand_id=paperbrand_id).paperbrand
    paperweights_cover = list(PaperWeights.objects.filter(paperbrand=paperbrand).values())
    return JsonResponse({'data': paperweights_cover})


# dropdown papercolor fill cover
def get_json_cover_papercolor(request, **kwargs):
    paperweight_id = kwargs.get('paperweight_id')
    exclusive_producer_id = define_exclusive_producer_id(request.user)
    paperweight_data = PaperWeights.objects.get(paperweight_id=paperweight_id)
    paperweight_m2 = paperweight_data.paperweight_m2
    paperbrand = paperweight_data.paperbrand
    papercolors_cover = list(PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight_m2).values())
    return JsonResponse({'data': papercolors_cover})
