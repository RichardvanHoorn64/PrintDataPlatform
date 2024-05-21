from django.http import JsonResponse
from methods.models import *


def get_json_folder_number_of_pages(request, **kwargs):
    foldingmethod_id = kwargs.get('foldingmethod_id')
    try:
        number_of_pages = FoldingMethods.objects.get(foldingmethod_id=foldingmethod_id).number_of_pages
        return JsonResponse({'data': number_of_pages})
    except ValueError:
        pass

