from django.http import JsonResponse
from methods.models import *


def get_json_folder_number_of_pages(request, **kwargs):
    foldingmethod_id = kwargs.get('foldingmethod_id')
    try:
        number_of_pages = FoldingMethods.objects.get(foldingmethod_id=foldingmethod_id).number_of_pages
        return JsonResponse({'data': number_of_pages})
    except ValueError:
        pass


def get_json_brochure_finishingmethods(request, **kwargs):
    user = request.user
    productcategory = kwargs.get('productcategory_id')
    try:
        brochure_finishingmethods = list(BrochureFinishingMethods.objects.filter(productcategory=productcategory).values().order_by('finishingmethod_id'))
        return JsonResponse({'data': brochure_finishingmethods})
    except ValueError:
        pass
