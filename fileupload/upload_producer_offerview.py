from azure.storage.blob import BlobServiceClient
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import TemplateView
from index.create_context import creatememberplan_context
from index.translate_functions import *
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from offers.models import Offers
from .forms import UploadFileForm
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from printdataplatform.settings import *
from azure.identity import ManagedIdentityCredential, DefaultAzureCredential


def validate_pdf(file):
    if not file.name.endswith('.pdf'):
        raise ValidationError('Het bestand moet een PDF zijn.')


def handle_uploaded_file(f):
    # Hier wordt het bestand opgeslagen naar Azure Blob Storage via de default_storage
    path = default_storage.save(f.name, ContentFile(f.read()))
    return path


def upload_producer_offerfile(request):
    if request.method == 'POST' and request.FILES['file']:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            handle_uploaded_file(uploaded_file)
            return HttpResponse('Bestand succesvol geüpload!')
    else:
        form = UploadFileForm()

    return render(request, 'fileupload/upload_producer_offerfile.html', {'form': form})


class UploadProducerOffer(LoginRequiredMixin, TemplateView):
    template = 'producers/assortiment_upload.html'
    template_name = 'fileupload/upload_producer_offerfile.html'
    form_class = UploadFileForm()
    success_url = '/producer_assortiment/'
    instruction = 'Upload de pdf file met offerte van de aanbieder voor dit project ;'
    upload_date = timezone.now().today().date()

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs['offer_id']

        if not user.is_authenticated:
            return redirect('/home/')
        elif not user.member.active:
            return redirect('/wait_for_approval/')
        # check access
        elif not Offers.objects.filter(producer_id=user.producer_id, offer_id=offer_id).exists():
            return redirect('/no_access/')
        else:
            return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        error = []
        pdf_file = []
        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)

        if not error:
            try:
                pdf_file = self.request.FILES['file']

            except Exception as e:

                error = 'Laad een PDF file : ' + str(e)
                print("error: ", error)

        # Valideer of het bestand een PDF is
        try:
            validate_pdf(pdf_file)
        except ValidationError as e:
            error = 'pdf validation error: ' + str(e)

        if not error:
            try:
                if not pdf_file.name.endswith('.pdf'):
                    error = 'Alleen een PDF file toegestaan'
                    print("error: ", error)
                else:
                    error = []
            except Exception as e:
                error = 'File load error: ' + str(e)
                print("error: ", error)

            # if file is too large, return
            if not error:
                try:
                    if pdf_file.multiple_chunks():
                        error = "Your uploaded file is too big, please refresh page and try again"

                except Exception as e:
                    error = 'Error: Your uploaded file is too big, please refresh page and try again: ' + str(e)
                    print("error: ", error)

        if not error:

            # Blob Storage details
            file_name = pdf_file.name
            blob_name = str(offer_id) + '_' + file_name
            account_name = AZURE_STORAGE_ACCOUNT_NAME
            container_name = "produceroffers"

            # Create credential
            try:
                if DEBUG:
                    credential = AZURE_STORAGE_ACCOUNT_KEY
                else:
                    credential = ManagedIdentityCredential(client_id=AZURE_CLIENT_ID)
            except Exception as e:
                error = 'Credential error: ' + str(e)
                return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + error)

            try:
                blob_service_client = BlobServiceClient(
                    account_url=f"https://{account_name}.blob.core.windows.net",
                    credential=credential
                )
            except Exception as e:
                error = 'Blob_service_client error: ' + str(e)
                return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + error)

            # Create container_client
            try:
                container_client = blob_service_client.get_container_client(container_name)
                # Create container if not exist
                if not container_client.exists():
                    container_client.create_container()
            except Exception as e:
                error = 'Container client error: ' + str(e)
                return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + error)

            # Upload file to container
            try:
                blob_client = container_client.get_blob_client(blob_name)
                blob_client.upload_blob(pdf_file, overwrite=True)
            except Exception as e:
                error = 'Blob upload error: ' + str(e)
                return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + error)

            print('File uploaded to Azure Blob Storage:', str(blob_name))

            # save metadata
            offer.doc_name = file_name
            offer.doc_uploaded = True
            offer.save()

            return redirect('/offer_details/' + str(offer.offer_id))

    def get_context_data(self, **kwargs):
        context = super(UploadProducerOffer, self).get_context_data(**kwargs)
        user = self.request.user
        context = creatememberplan_context(context, user)

        error = self.kwargs['error']
        if error == 'None':
            error_message = False
        else:
            error_message = True

        offer_id = self.kwargs['offer_id']
        offer = Offers.objects.get(offer_id=offer_id)
        producer = Producers.objects.get(producer_id=offer.producer_id)
        member = Members.objects.get(member_id=offer.member_id)
        context['offer'] = offer
        context['producer'] = producer
        context['member'] = member
        context['messages'] = messages
        context['error_text'] = error
        context['error_message'] = error_message
        return context
