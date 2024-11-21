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
from azure.identity import ManagedIdentityCredential
from azure.storage.blob import BlobClient


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
            try:
                # Replace with your Blob Storage details
                file_name = pdf_file.name
                blob_name = str(offer_id) + '_' + file_name
                account_name = AZURE_STORAGE_ACCOUNT_NAME
                container_name = "produceroffers"

                # Construct the Blob URL

                if DEBUG:
                    account_key = AZURE_STORAGE_ACCOUNT_KEY
                    # Azure Blob Storage configuraties instellen
                    # Verbinden met de Azure Blob Storage service
                    blob_service_client = BlobServiceClient(account_url=f"https://{account_name}.blob.core.windows.net",
                                                            credential=account_key)

                    # Maak de container als die nog niet bestaat
                    container_client = blob_service_client.get_container_client(container_name)
                    if not container_client.exists():
                        container_client.create_container()

                    # De 'locatie' in de blob storage (inclusief de naam van het bestand)
                    blob_name = pdf_file.name

                    # Upload het bestand naar de container
                    blob_client = container_client.get_blob_client(blob_name)
                    blob_client.upload_blob(pdf_file, overwrite=True)  # Overwrite als het bestand al bestaat

                    print('message: Bestand succesvol geüpload naar Azure Blob Storage: {blob_name}')

                else:
                    # Construct the Blob URL
                    blob_url = f"https://{account_name}.blob.core.windows.net/{container_name}/{blob_name}"
                    # Use Managed Identity Credential
                    credential = ManagedIdentityCredential()
                    # Create BlobClient
                    blob_client = BlobClient(blob_url, credential=credential, blob_name=blob_name,
                                             container_name=container_name)

                    # upload blob
                    blob_client.upload_blob(pdf_file, overwrite=True)

                # save metadata
                offer.doc_name = file_name
                offer.doc_uploaded = True
                offer.save()

                print('message: Bestand succesvol geüpload naar Azure Blob Storage: {blob_name}')
            except Exception as e:
                print('error:, status=500, ' + str(e))
                return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + str(e))
        else:
            print('producer offer upload error: ', error)
            return redirect("/upload_producer_offerfile/" + str(offer.offer_id) + '/' + str(error))

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
