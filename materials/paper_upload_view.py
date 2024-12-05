import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils import timezone
from index.site_startfunctions import define_site_name
from materials.models import PaperBrandReference, PaperCatalog
from materials.papercatalog_uploadform import UploadProducerPaperCatalogCSVForm
from profileuseraccount.models import Producers


class UploadProducerPaperCatalog(LoginRequiredMixin, TemplateView):
    template = "materials/paper_producer_catalog_upload.html"
    form_class = UploadProducerPaperCatalogCSVForm
    success_url = '/paper_catalog/'
    instruction = 'Use CSV file UTF-8 with header and comma separated'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        user = self.request.user
        producer_id = user.producer_id
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)
        site_name = define_site_name(user)

        if paper_catalog:
            count_paper_catalog = paper_catalog.count()
            latest_upload = paper_catalog[1].upload_date
        else:
            count_paper_catalog = 0
            latest_upload = 'Nu papercatalog loaded'

        producer = Producers.objects.get(producer_id=user.producer_id)

        return render(request, self.template, {'form': form,
                                               'instruction': self.instruction,
                                               'count_paper_catalog': count_paper_catalog,
                                               'latest_upload': latest_upload,
                                               'member_plan_id': user.member_plan_id,
                                               'free_memberplans': [1, 3],
                                               'pro_memberplans': [2],
                                               'non_exclusive_memberplans': [1, 2],
                                               'exclusive_memberplans': [3],
                                               'open_memberplans': [1, 2, 3],
                                               'producer_memberplans': [4],
                                               'producer': producer,
                                               'site_name': site_name
                                               })

    def post(self, request, *args, **kwargs):
        form = self.form_class
        producer_id = self.request.user.producer_id
        name = self.request.user.first_name + " " + self.request.user.last_name
        upload_date = timezone.now().today().date()
        paper_catalog = PaperCatalog.objects.filter(producer_id=producer_id)
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

            new_catalog = pd.read_csv(csv_file, delimiter=';', header=0, encoding='latin-1')
            new_catalog['producer_id'] = producer_id

            decimal_columns = ['paper_thickening', 'price_1000sheets']

            for col in decimal_columns:
                new_catalog[col] = round(new_catalog[col].replace(',', '.', regex=True).astype(float), 2)

            # integer_columns = ['paperweight_m2', 'paper_height_mm', 'paper_width_mm']

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

        return redirect('/paper_catalog/',
                        {'form': form,
                         'last_upload': upload_date,
                         'success_message': 'File succesfull stored',
                         })
