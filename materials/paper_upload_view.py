import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import render, redirect
from django.utils import timezone
from materials.models import PaperBrandReference, PaperCatalog
from materials.papercatalog_uploadform import UploadProducerPaperCatalogCSVForm


class UploadProducerPaperCatalog(LoginRequiredMixin, View):
    template = "materials/paper_producer_catalog_upload.html"
    form_class = UploadProducerPaperCatalogCSVForm
    success_url = '/paper_catalog/'
    instruction = 'Use CSV file UTF-8 with header and comma separated'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        user = self.request.user
        producer_id = user.producer_id
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)

        if paper_catalog:
            count_paper_catalog = paper_catalog.count()
            latest_upload = paper_catalog[1].upload_date
        else:
            count_paper_catalog = 0
            latest_upload = 'Nu papercatalog loaded'

        return render(request, self.template, {'form': form,
                                               'instruction': self.instruction,
                                               'count_paper_catalog': count_paper_catalog,
                                               'latest_upload': latest_upload,
                                               })

    def post(self, request, *args, **kwargs):
        form = self.form_class
        producer_id = self.request.user.producer_id
        name = self.request.user.first_name + " " + self.request.user.last_name
        upload_date = timezone.now().today().date()
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)
        paper_catalog_general = PaperCatalog.objects.filter(producer_id=producer_id, source_id=1)
        error = []
        instruction_csv = 'Your file is not CSV type, please refresh page and try again'

        if paper_catalog:
            count_paper_catalog = paper_catalog.count()
            latest_upload = paper_catalog[1].upload_date
        else:
            count_paper_catalog = 0
            latest_upload = 'Load papercatalog using a csv file'

        try:
            csv_file = self.request.FILES['paper_catalog_file']  # .read().decode("utf-8")

            # if file is not csv file, return
            if not csv_file.name.endswith('.csv'):
                error = 'Error: Your file is not CSV type'

            # if file is too large, return
            if csv_file.multiple_chunks():
                error = 'Error: Your uploaded file is too big (> MB)'

            if error:
                return render(request, self.template, {'form': form,
                                                       'instruction': instruction_csv,
                                                       'count_paper_catalog': count_paper_catalog,
                                                       'latest_upload': latest_upload,
                                                       'error': error,
                                                       })

        except Exception as e:
            print('error e: ' + str(e))

            return render(request, self.template, {'form': form,
                                                   'instruction': instruction_csv,
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # delete producer papercatalog records
        try:
            # delete producer papercatalog records
            old_catalog = paper_catalog
            for old_item in old_catalog:
                old_item.delete()

            # delete general papercatalog records
            old_catalog_general = paper_catalog_general
            for old_item_general in old_catalog_general:
                old_item_general.delete()

            new_catalog = pd.read_csv(csv_file, delimiter=';', header=0, encoding='latin-1')
            new_catalog['producer_id'] = producer_id

            decimal_columns = ['paper_thickening', 'price_1000sheets']
            integer_columns = ['paperweight_m2', 'paper_height_mm', 'paper_width_mm']

            for col in decimal_columns:
                new_catalog[col] = round(new_catalog[col].replace(',', '.', regex=True).astype(float), 2)
            #
            # for col in integer_columns:
            #     if new_catalog[col] is None:
            #         new_catalog[col] = 0
            #     try:
            #         new_catalog[col] = new_catalog[col].astype(int)
            #     except Exception as e:
            #         print('error e: ' + str(e))

            # replace exclusive producer catalog
            for index, row in new_catalog.iterrows():
                new_paperspecs = PaperCatalog(
                    producer_id=producer_id,
                    source_id=producer_id,
                    uploaded_by=name,
                    upload_date=upload_date,
                    supplier=row['supplier'],
                    supplier_number=row['supplier_number'],
                    papercategory=row['papercategory'],
                    paperbrand=row['paperbrand'],
                    papercolor=row['papercolor'],
                    paperweight_m2=row['paperweight_m2'],
                    paper_height_mm=row['paper_height_mm'],
                    paper_width_mm=row['paper_width_mm'],
                    paper_surface=row['paper_height_mm'] * row['paper_width_mm'],
                    fiber_direction=row['fiber_direction'],
                    paper_thickening=row['paper_thickening'],
                    singe_sided=row['singe_sided'],
                    sheets_per_pack=row['sheets_per_pack'],
                    price_1000sheets=row['price_1000sheets'],

                )
                try:
                    new_paperspecs.save()
                except ValueError:
                    pass

            # update exclusive producer catalog
            if producer_id > 1:
                for index, row in new_catalog.iterrows():
                    new_paperspecs_general = PaperCatalog(
                        producer_id=1,
                        source_id=producer_id,
                        uploaded_by=name,
                        upload_date=upload_date,
                        supplier=row['supplier'],
                        supplier_number=row['supplier_number'],
                        papercategory=row['papercategory'],
                        paperbrand=row['paperbrand'],
                        papercolor=row['papercolor'],
                        paperweight_m2=row['paperweight_m2'],
                        paper_height_mm=row['paper_height_mm'],
                        paper_width_mm=row['paper_width_mm'],
                        paper_surface=row['paper_height_mm'] * row['paper_width_mm'],
                        fiber_direction=row['fiber_direction'],
                        paper_thickening=row['paper_thickening'],
                        singe_sided=row['singe_sided'],
                        sheets_per_pack=row['sheets_per_pack'],
                        price_1000sheets=row['price_1000sheets'],
                    )
                    try:
                        new_paperspecs_general.save()
                    except ValueError:
                        pass

            # Update paperbrandreference

            new_paperbrands = PaperCatalog.objects.filter(producer_id=producer_id).distinct('paperbrand').values_list(
                'paperbrand', flat=True)
            exist_paperbrands = PaperBrandReference.objects.filter(producer_id=producer_id).values_list('paperbrand',
                                                                                                        flat=True)
            for paperbrand in new_paperbrands:
                if paperbrand not in exist_paperbrands:
                    papercategory = PaperCatalog.objects.filter(producer_id=producer_id,
                                                                paperbrand=paperbrand).values_list('papercategory',
                                                                                                   flat=True).first()
                    new_paperbrand = PaperBrandReference(
                        producer_id=producer_id,
                        papercategory=papercategory,
                        paperbrand=paperbrand,
                    )

                    try:
                        new_paperbrand.save()
                    except ValueError:
                        pass

                    if producer_id > 1:
                        new_paperbrand_general = PaperBrandReference(
                            producer_id=1,
                            papercategory=papercategory,
                            paperbrand=paperbrand,
                        )
                        try:
                            new_paperbrand_general.save()
                        except ValueError:
                            pass

            if producer_id > 1:
                for paperbrand in exist_paperbrands:
                    if paperbrand not in new_paperbrands:
                        PaperBrandReference(producer_id=producer_id, paperbrand=paperbrand).delete()

        except Exception as e:
            error = 'papercatalog not loaded, error:' + str(e)
            print(error)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Contact site administrator for help',
                                                   'count_paper_catalog': count_paper_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # papercategory dropdown
        # try:
        #     old_papercategories = PaperCategories.objects.filter(producer_id=producer_id)
        #     for old_papercategory in old_papercategories:
        #         old_papercategory.delete()
        #
        #     new_papercategorylist = pd.DataFrame(
        #         new_catalog[['producer_id', 'papercategory']].drop_duplicates())
        #
        #     for index, row in new_papercategorylist.iterrows():
        #         if len(PaperCategories.objects.filter(papercategory=row['papercategory'],producer_id=producer_id)) == 0:
        #             new_papercategory = PaperCategories(
        #                 papercategory=row['papercategory'],
        #                 producer_id=row['producer_id'],
        #             )
        #             new_papercategory.save()
        #
        #     for index, row in new_papercategorylist.iterrows():
        #         if len(PaperCategories.objects.filter(papercategory=row['papercategory'],producer_id=None)) == 0:
        #             new_general_papercategory = PaperCategories(
        #                 papercategory=row['papercategory'],
        #             )
        #             new_general_papercategory.save()
        #
        # except Exception as e:
        #     error = 'Papercategories not loaded:' + str(e)
        #     print(error)
        #     return render(request, self.template, {'form': form,
        #                                            'instruction': 'Correct file, please refresh page and try again',
        #                                            'count_paper_catalog': count_paper_catalog,
        #                                            'latest_upload': latest_upload,
        #                                            'error': error,
        #                                           })

        # paperbrand dropdown
        # try:
        #     old_paperbands = PaperBrands.objects.filter(producer_id=producer_id)
        #     for old_paperband in old_paperbands:
        #         old_paperband.delete()
        #
        #     new_paperbandlist = pd.DataFrame(
        #         new_catalog[['producer_id', 'papercategory', 'paperbrand']].drop_duplicates())
        #
        #     for index, row in new_paperbandlist.iterrows():
        #         new_paperbands = PaperBrands(
        #             producer_id=row['producer_id'],
        #             upload_date=upload_date,
        #             papercategory=row['papercategory'],
        #             paperbrand=row['paperbrand'],
        #         )
        #         new_paperbands.save()
        #
        #     for index, row in new_paperbandlist.iterrows():
        #         if len(PaperBrands.objects.filter(papercategory=row['papercategory'],paperbrand=row['paperbrand'], producer_id=None)) == 0:
        #             new_general_paperbrand = PaperBrands(
        #                 upload_date=upload_date,
        #                 papercategory=row['papercategory'],
        #                 paperbrand=row['paperbrand'],
        #             )
        #             new_general_paperbrand.save()

        # except Exception as e:
        #     error = 'Paperbrands not loaded:' + str(e)
        #     print(error)
        #     return render(request, self.template, {'form': form,
        #                                            'instruction': 'Correct file, please refresh page and try again',
        #                                            'count_paper_catalog': count_paper_catalog,
        #                                            'latest_upload': latest_upload,
        #                                            'error': error,
        #                                            })

        # paperweights dropdown
        # try:
        #     old_paperweights = PaperWeights.objects.filter(producer_id=producer_id)
        #     for old_paperweight in old_paperweights:
        #         old_paperweight.delete()
        #
        #     new_paperweightslist = pd.DataFrame(
        #         new_catalog[['producer_id', 'papercategory', 'paperbrand', 'paperweight_m2']].drop_duplicates())
        #
        #     for index, row in new_paperweightslist.iterrows():
        #         new_paperweights = PaperWeights(
        #             producer_id=row['producer_id'],
        #             upload_date=upload_date,
        #             papercategory=row['papercategory'],
        #             paperbrand=row['paperbrand'],
        #             paperweight_m2=row['paperweight_m2'],
        #         )
        #         new_paperweights.save()
        #
        #     for index, row in new_paperweightslist.iterrows():
        #         if len(PaperWeights.objects.filter(papercategory=row['papercategory'],paperbrand=row['paperbrand'], paperweight_m2=row['paperweight_m2'], producer_id=None)) == 0:
        #             new_general_paperweight = PaperWeights(
        #                 upload_date=upload_date,
        #                 papercategory=row['papercategory'],
        #                 paperbrand=row['paperbrand'],
        #                 paperweight_m2=row['paperweight_m2'],
        #             )
        #             new_general_paperweight.save()
        #
        # except Exception as e:
        #     error = 'New_paperweights not loaded:' + str(e)
        #     print('error new_paperweights not loaded:', e)
        #     return render(request, self.template, {'form': form,
        #                                            'instruction': 'Contact site administrator for help',
        #                                            'count_paper_catalog': count_paper_catalog,
        #                                            'latest_upload': latest_upload,
        #                                            'error': error,
        #                                            })

        # end procedure
        return redirect('/paper_catalog/',
                        {'form': form,
                         'last_upload': upload_date,
                         'success_message': 'File succesfull stored',
                         })
