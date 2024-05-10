from django.http import JsonResponse
from materials.models import *


# dropdown papercategory
def get_json_papercategory(request, **kwargs):
    productcategory_id = kwargs.get('productcategory_id')
    papercategories = list(
        PaperCategoryReference.objects.all().values().order_by('papercategory_id'))
    # papercategories = list(
    #     PaperCategoryReference.objects.filter(prodoductcatogory_id__contains=productcategory_id).values().order_by(
    #         'papercategory'))
    return JsonResponse({'data': papercategories})


# dropdown paperbrand
def get_json_paperbrand(request, **kwargs):
    papercategory_id = kwargs.get('papercategory_id')
    papercategory = PaperCategoryReference.objects.get(papercategory_id=papercategory_id).papercategory
    paperbrands = list(PaperBrand.objects.filter(papercategory=papercategory).values().order_by('paperbrand'))
    return JsonResponse({'data': paperbrands})


# dropdown paperweight
def get_json_paperweight(request, **kwargs):
    paperbrand_id = kwargs.get('paperbrand_id')
    productcategory_id = kwargs.get('productcategory_id')

    # Plano
    if productcategory_id == 1:
        max_weight = 600
    # Folders
    elif productcategory_id == 2:
        max_weight = 250
    # Brochures interior
    elif productcategory_id in ["3", "4", "5", ]:
        max_weight = 150
    else:
        max_weight = 1000

    paperbrand = PaperBrand.objects.get(paperbrand_id=paperbrand_id).paperbrand
    paperweights = list(
        PaperWeights.objects.filter(paperbrand=paperbrand, paperweight_m2__lte=max_weight).values().order_by(
            'paperweight_m2'))
    return JsonResponse({'data': paperweights})


# dropdown papercolor
def get_json_papercolor(request, **kwargs):
    paperweight_id = kwargs.get('paperweight_id')
    paperweight_data = PaperWeights.objects.get(paperweight_id=paperweight_id)
    paperweight_m2 = paperweight_data.paperweight_m2
    paperbrand = paperweight_data.paperbrand
    papercolors = list(PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight_m2).values())
    return JsonResponse({'data': papercolors})


# For brochures covers

# dropdown papercategory cover
def get_json_cover_papercategory(request, **kwargs):
    papercategories_cover = list(PaperCategoryReference.objects.filter(brochures_cover=True).values().order_by('papercategory'))
    return JsonResponse({'data': papercategories_cover})


# dropdown paperweight fill cover
def get_json_cover_paperbrand(request, **kwargs):
    papercategory_id = kwargs.get('papercategory_id')
    papercategory = PaperCategoryReference.objects.get(papercategory_id=papercategory_id).papercategory
    paperbrands_cover = list(PaperBrand.objects.filter(papercategory=papercategory).values().order_by('paperbrand'))
    return JsonResponse({'data': paperbrands_cover})


def get_json_cover_paperweight(request, **kwargs):
    paperbrand_id = kwargs.get('paperbrand_id')
    paperbrand = PaperBrand.objects.get(paperbrand_id=paperbrand_id).paperbrand
    paperweights_cover = list(PaperWeights.objects.filter(paperbrand=paperbrand).values())
    return JsonResponse({'data': paperweights_cover})


# dropdown papercolor fill cover
def get_json_cover_papercolor(request, **kwargs):
    paperweight_id = kwargs.get('paperweight_id')
    paperweight_data = PaperWeights.objects.get(paperweight_id=paperweight_id)
    paperweight_m2 = paperweight_data.paperweight_m2
    paperbrand = paperweight_data.paperbrand
    papercolors_cover = list(PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight_m2).values())
    return JsonResponse({'data': papercolors_cover})
