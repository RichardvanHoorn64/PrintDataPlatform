from django.http import JsonResponse
from django.shortcuts import redirect
from materials.models import *


# dropdown paperbrand
def get_json_paperbrand(request, **kwargs):
    if request.user.is_authenticated:
        papercategory = kwargs.get('papercategory')
        paperbrands = list(
            PaperCatalog.objects.filter(papercategory=papercategory, producer_id=1).values().distinct(
                'paperbrand').order_by('paperbrand'))
        return JsonResponse({'data': paperbrands})
    else:
        return redirect('/home/')


# dro pdown paperweight
def get_json_paperweight(request, **kwargs):
    if request.user.is_authenticated:
        paperbrand = kwargs.get('paperbrand')
        paperweights = list(
            PaperCatalog.objects.filter(paperbrand=paperbrand, producer_id=1).values().distinct(
                'paperweight_m2').order_by('paperweight_m2'))
        return JsonResponse({'data': paperweights})
    else:
        return redirect('/home/')


# dropdown papercolor
def get_json_papercolor(request, **kwargs):
    if request.user.is_authenticated:
        paperbrand = kwargs.get('paperbrand')
        paperweight = kwargs.get('paperweight')
        papercolors = list(
            PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight,
                                        producer_id=1).values().distinct(
                'papercolor').order_by('papercolor'))
        return JsonResponse({'data': papercolors})
    else:
        return redirect('/home/')


# For brochures covers
def get_json_cover_paperbrand(request, **kwargs):
    if request.user.is_authenticated:
        papercategory = kwargs.get('papercategory')
        paperbrands_cover = list(
            PaperCatalog.objects.filter(papercategory=papercategory, producer_id=1).values().distinct(
                'paperbrand').order_by('paperbrand'))
        return JsonResponse({'data': paperbrands_cover})
    else:
        return redirect('/home/')


def get_json_cover_paperweight(request, **kwargs):
    if request.user.is_authenticated:
        paperbrand = kwargs.get('paperbrand')
        paperweights_cover = list(
            PaperCatalog.objects.filter(paperbrand=paperbrand, producer_id=1).values().distinct(
                'paperweight_m2').order_by('paperweight_m2'))
        return JsonResponse({'data': paperweights_cover})
    else:
        return redirect('/home/')


# dropdown papercolor fill cover
def get_json_cover_papercolor(request, **kwargs):
    if request.user.is_authenticated:
        paperbrand = kwargs.get('paperbrand')
        paperweight = kwargs.get('paperweight')
        papercolors_cover = list(
            PaperCatalog.objects.filter(paperbrand=paperbrand, paperweight_m2=paperweight,
                                        producer_id=1).values().distinct(
                'papercolor').order_by('papercolor'))
        return JsonResponse({'data': papercolors_cover})
    else:
        return redirect('/home/')


# For envelopes
# get size and cut
def get_json_env_size_close_cut(request, **kwargs):
    if request.user.is_authenticated:
        env_category_id = kwargs.get('env_category_id')
        env_size_close_cut_list = list(
            EnvelopeCatalog.objects.filter(env_category_id=env_category_id, producer_id=1).values().distinct(
                'env_size_close_cut', 'env_category_id').order_by('env_category_id'))
        return JsonResponse({'data': env_size_close_cut_list})
    else:
        return redirect('/home/')


# env dropdown get material and color
def get_json_env_material_color(request, **kwargs):
    if request.user.is_authenticated:
        env_category_id = kwargs.get('env_category_id')
        env_size_close_cut = kwargs.get('env_size_close_cut')
        paperweights_cover = list(
            EnvelopeCatalog.objects.filter(env_category_id=env_category_id, env_size_close_cut=env_size_close_cut,
                                        producer_id=1).values().distinct(
                'env_material_color').order_by('env_material_color'))
        return JsonResponse({'data': paperweights_cover})
    else:
        return redirect('/home/')


# dropdown papercolor get window
def get_json_env_window(request, **kwargs):
    if request.user.is_authenticated:
        env_category_id = kwargs.get('env_category_id')
        env_size_close_cut = kwargs.get('env_size_close_cut')
        env_material_color = kwargs.get('env_material_color')
        papercolors_cover = list(
            EnvelopeCatalog.objects.filter(env_category_id=env_category_id, env_size_close_cut=env_size_close_cut,
                                        env_material_color=env_material_color,
                                        producer_id=1).values().distinct(
                'env_window').order_by('env_window'))
        return JsonResponse({'data': papercolors_cover})
    else:
        return redirect('/home/')
