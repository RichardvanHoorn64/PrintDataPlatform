from django.shortcuts import render

producentnaam = ''


def test_papier_empty(self, skin_template_name, persen, oplage, productgroep, omschrijving):
    if persen.empty:
        return render(self.request, 'geen_aanbieding.html',
                      {'bericht': 'Geen passende drukpersen bij uw drukkerij beschikbaar, '
                                  'passend bij deze aanvraag, neem contact op met '  'neem contact op met ' + str(
                          producentnaam),
                       'skin_template_name': skin_template_name,
                       'oplage': oplage,
                       'productgroep': productgroep,
                       'omschrijving': omschrijving,
                       })


def test_persen_empty(self, skin_template_name, persen, oplage, productgroep, omschrijving):
    if persen.empty:
        return render(self.request, 'geen_aanbieding.html',
                      {'bericht': 'Geen passende drukpersen bij uw drukkerij beschikbaar, '
                                  'passend bij deze aanvraag, neem contact op met ',
                       'skin_template_name': skin_template_name,
                       'oplage': oplage,
                       'productgroep': productgroep,
                       'omschrijving': omschrijving,
                       })
