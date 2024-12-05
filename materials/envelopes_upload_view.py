import pandas as pd
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.utils import timezone
from index.site_startfunctions import define_site_name
from materials.models import EnvelopeCatalog, EnvelopeCategory
from materials.envelopescatalog_uploadform import UploadProducerEnvelopesCatalogCSVForm
from profileuseraccount.models import Producers


class UploadProducerEnvelopesCatalog(LoginRequiredMixin, TemplateView):
    template = 'materials/envelopes_producer_catalog_upload.html'

    form_class = UploadProducerEnvelopesCatalogCSVForm
    success_url = '/envelopes_catalog/'
    instruction = 'Use CSV file UTF-8 with header and comma separated'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        user = self.request.user
        producer_id = user.producer_id
        envelopes_catalog = EnvelopeCatalog.objects.filter(producer_id=producer_id)
        site_name = define_site_name(user)

        if envelopes_catalog:
            count_envelopes_catalog = envelopes_catalog.count()
            latest_upload = envelopes_catalog[0].upload_date
        else:
            count_envelopes_catalog = 0
            latest_upload = 'EnvelopeCatalog loaded'

        producer = Producers.objects.get(producer_id=user.producer_id)

        return render(request, self.template, {'form': form,
                                               'instruction': self.instruction,
                                               'count_envelopes_catalog': count_envelopes_catalog,
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
        envelopes_catalog = EnvelopeCatalog.objects.filter(producer_id=producer_id)
        envelopes_categories = EnvelopeCategory.objects.filter(producer_id=producer_id)
        error = []
        instruction_csv = 'Your file is not CSV type, please refresh page and try again'

        if envelopes_catalog:
            count_envelopes_catalog = envelopes_catalog.count()
            # latest_upload = envelopes_catalog[1].upload_date
        else:
            count_envelopes_catalog = 0
            # latest_upload = 'Load EnvelopeCatalog using a csv file'
        latest_upload = []

        try:
            csv_file = self.request.FILES['envelopes_catalog_file']  # .read().decode("utf-8")

            # if file is not csv file, return
            if not csv_file.name.endswith('.csv'):
                error = 'Error: Your file is not CSV type'

            # if file is too large, return
            if csv_file.multiple_chunks():
                error = 'Error: Your uploaded file is too big (> MB)'

            if error:
                return render(request, self.template, {'form': form,
                                                       'instruction': instruction_csv,
                                                       'count_envelopes_catalog': count_envelopes_catalog,
                                                       'latest_upload': latest_upload,
                                                       'error': error,
                                                       })

        except Exception as e:
            print('error e: ' + str(e))

            return render(request, self.template, {'form': form,
                                                   'instruction': instruction_csv,
                                                   'count_envelopes_catalog': count_envelopes_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        # delete producer EnvelopeCatalog records
        try:
            # delete producer EnvelopeCatalog records
            old_catalog = envelopes_catalog
            for old_item in old_catalog:
                old_item.delete()

            new_catalog = pd.read_csv(csv_file, delimiter=';', header=0, encoding='latin-1')
            new_catalog['producer_id'] = producer_id

            decimal_columns = ['price_1000_envelopes']
            # integer_columns = ['env_weight_m2', 'paper_height_mm', 'paper_width_mm']

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

            new_categories = new_catalog[['env_category', 'env_category_name']].drop_duplicates()

            # replace producer categories
            # delete EnvelopeCategory records
            # old_envelopes_categories = envelopes_categories
            # for old_category in old_envelopes_categories:
            #     old_category.delete()
            #
            # for index, row in new_categories.iterrows():
            #     new_category_specs = EnvelopeCatalog(
            #         producer_id=producer_id,
            #         env_category_id=row['env_category'],
            #         env_category_name=row['env_category_name'],
            #     )
            #     try:
            #         new_category_specs.save()
            #     except ValueError:
            #         pass

            # replace exclusive producer catalog
            for index, row in new_catalog.iterrows():

                new_paperspecs = EnvelopeCatalog(
                    producer_id=producer_id,
                    env_category_id=row['env_category'],
                    supplier=row['supplier'],
                    supplier_number=row['supplier_number'],
                    env_category_name=row['env_category_name'],
                    env_paper=row['env_paper'],
                    env_color=row['env_color'],
                    env_interior=row['env_interior'],
                    env_size=row['env_size'],
                    env_width_mm=row['env_width_mm'],
                    env_height_mm=row['env_height_mm'],
                    env_weight_m2=row['env_weight_m2'],
                    env_die_cut=row['env_die_cut'],
                    env_closure=row['env_closure'],
                    env_window_orientation=row['env_window_orientation'],
                    env_window_size=row['env_window_size'],
                    env_window_position=row['env_window_position'],
                    FSC=row['FSC'],
                    # dropdowns
                    env_size_close_cut=str(row['env_size']) + ", sluiting " + str(row['env_closure']) + ", snit " + str(
                        row['env_die_cut']),
                    env_material_color=str(row['env_weight_m2']) + "gr m2 ," + str(row['env_paper']) + ", " + row[
                        'env_color'] + ", binnendruk " + str(row['env_interior']),
                    env_window=str(row['env_window_orientation']) + " venster: " + str(
                        row['env_window_size']) + " positie: " + str(row['env_window_position']),

                    envelopes_per_pack=row['envelopes_per_pack'],
                    price_1000_envelopes=row['price_1000_envelopes'],
                    uploaded_by=name,
                    upload_date=upload_date,

                )
                try:
                    new_paperspecs.save()
                except ValueError:
                    pass

                try:
                    envelopes_catalog_no_window = EnvelopeCatalog.objects.filter(producer_id=producer_id)
                    for env_no_window in envelopes_catalog_no_window:
                        if env_no_window.env_window_orientation =='Geen':
                            env_no_window.env_window = 'Geen venster'
                            env_no_window.save()
                except ValueError:
                    pass

        except Exception as e:
            error = 'EnvelopeCatalog not loaded, error:' + str(e)
            print(error)
            return render(request, self.template, {'form': form,
                                                   'instruction': 'Contact site administrator for help',
                                                   'count_envelopes_catalog': count_envelopes_catalog,
                                                   'latest_upload': latest_upload,
                                                   'error': error,
                                                   })

        return redirect('/envelopes_catalog/',
                        {'form': form,
                         'last_upload': upload_date,
                         'success_message': 'File succesfull stored',
                         })
