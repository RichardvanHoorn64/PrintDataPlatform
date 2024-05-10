from django.core.mail import send_mail


def form_invalid_message_quotes(form, response):
    print("form is invalid, response :", response)
    print("form errors :", form.errors)
    print("form cleaned_data :", form.cleaned_data)
    try:
        send_mail(
            'Form invalid offerteaanvraag:',
            "form is invalid, response :" + str(response) +
            "form errors :" + str(form.errors) +
            "form cleaned_data :" + str(form.cleaned_data),
            'info@richardvanhoorn.nl',
            ['info@richardvanhoorn.nl'],
            fail_silently=False,
        )
    except Exception as e:
        print('form invalid message error: ', e,
              'Form invalid offerte:',
              "form is invalid, response :" + str(response) +
              "form errors :" + str(form.errors) +
              "form cleaned_data :" + str(form.cleaned_data))
        pass
