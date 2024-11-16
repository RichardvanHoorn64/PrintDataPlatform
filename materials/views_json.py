from django.http import JsonResponse
from materials.models import *


# dropdown paperbrand
def get_json_paperbrand(request, **kwargs):
    user = request.user
    exclusive_producer_id = 1
    papercategory = kwargs.get('papercategory')
    paperbrands = list(
        PaperCatalog.objects.filter(papercategory=papercategory, producer_id=exclusive_producer_id).values().distinct(
            'paperbrand').order_by('paperbrand'))
    return JsonResponse({'data': paperbrands})


# dro pdown paperweight
def get_json_paperweight(request, **kwargs):
    paperbrand = kwargs.get('paperbrand')
    exclusive_producer_id = 1
    paperweights = list(
        PaperCatalog.objects.filter(paperbrand=paperbrand, producer_id=exclusive_producer_id).values().distinct(
            'paperweight_m2').order_by('paperweight_m2'))
    return JsonResponse({'data': paperweights})


# dropdown papercolor
def get_json_papercolor(request, **kwargs):
    exclusive_producer_id = 1
    paperbrand = kwargs.get('paperbrand')
    paperweight = kwargs.get('paperweight')
    papercolors = list(
        PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight,
                                    producer_id=exclusive_producer_id).values().distinct(
            'papercolor').order_by('papercolor'))
    return JsonResponse({'data': papercolors})


# For brochures covers
def get_json_cover_paperbrand(request, **kwargs):
    user = request.user
    exclusive_producer_id = 1
    papercategory = kwargs.get('papercategory')
    paperbrands_cover = list(
        PaperCatalog.objects.filter(papercategory=papercategory, producer_id=exclusive_producer_id).values().distinct(
            'paperbrand').order_by('paperbrand'))
    return JsonResponse({'data': paperbrands_cover})


def get_json_cover_paperweight(request, **kwargs):
    paperbrand = kwargs.get('paperbrand')
    exclusive_producer_id = 1
    paperweights_cover = list(
        PaperCatalog.objects.filter(paperbrand=paperbrand, producer_id=exclusive_producer_id).values().distinct(
            'paperweight_m2').order_by('paperweight_m2'))
    return JsonResponse({'data': paperweights_cover})


# dropdown papercolor fill cover
def get_json_cover_papercolor(request, **kwargs):
    exclusive_producer_id = 1
    paperbrand = kwargs.get('paperbrand')
    paperweight = kwargs.get('paperweight')
    papercolors_cover = list(
        PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight,
                                    producer_id=exclusive_producer_id).values().distinct(
            'papercolor').order_by('papercolor'))
    return JsonResponse({'data': papercolors_cover})
