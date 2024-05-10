portrait_landscape_choices = [
    {'type': 'staand'},
    {'type': 'liggend'},
    {'type': 'vierkant'},
]

printsided_choices = [
    {'type': 'Tweezijdig gelijk'},
    {'type': 'Eenzijdig'},
    {'type': 'Tweezijdig verschillend'},
]

print_choices = [
    {'type': 'Full Colour'},
    {'type': 'Zwart'},
    {'type': 'Alleen PMS kleuren'},
]

pressvarnish_choices = [
    {'type': 'Geen persvernis'},
    {'type': 'Persvernis'},
    {'type': 'Dispersielak'},
]

enhance_sided_choices = (
    {'type': 'Geen veredeling'},
    {'type': 'Tweezijdig gelijk'},
    {'type': 'Alleen voorzijde'},
    {'type': 'Alleen achterzijde'},
    {'type': 'Tweezijdig verschillend'},
)

enhance_choices = (
    {'type': 'Mat lak'},
    {'type': 'Glans lak'},
    {'type': 'Dispersie lak'},
    {'type': 'UV lak'},
    {'type': 'Mat lamineren'},
    {'type': 'Glans lamineren'},
    {'type': 'Krasvast mat lamineren'},
)

packaging_choices = [
    {'type': 'Handzaam in dozen'},
    {'type': 'Afgestapeld op pallets'},
    {'type': 'Gebundeld op pallets'},
    {'type': 'Gebundeld in dozen'},
    {'type': 'Per stuk gesealed'},
    {'type': 'Per stuk gesealed in dozen'},
]

finishing_brochures_choices = [
    {'type': 'Twee nietjes'},
    {'type': 'Twee oognieten'},
    {'type': 'Vier nietjes'},
    {'type': 'Vier oognieten'},
    {'type': 'Cahiersteek'},
    {'type': 'Singersteek'},
]

bedrukking_choicelist = [
    {'type': 'Zwart'},
    {'type': 'Full Colour'},
    {'type': 'Alleen PMS kleuren'},
]

bedrukking_choicelist_no_pms = [
    {'type': 'Full Colour'},
    {'type': 'Zwart'},
]

# algemene keuzelijst veredeling
veredeling_lijst = ['Mat lak', 'Glans lak', 'Dispersie lak', 'UV lak', 'Mat lamineren', 'Krasvast mat lamineren',
                    'Glans lamineren', ]

bedrukking_choicelist_clone = [
    {'type': 'Wijzig bedrukking'},
    {'type': 'Full Colour'},
    {'type': 'Zwart'},
    {'type': 'Alleen PMS kleuren'},
]

bedrukking_choicelist_clone_no_pms = [
    {'type': 'Wijzig bedrukking'},
    {'type': 'Full Colour'},
    {'type': 'Zwart'},
]

afloop_choicelist = [
    {'type': 'Ja'},
    {'type': 'Nee'},
]

afloop_choicelist_clone = [
    {'type': 'Aflopend wijzigen'},
    {'type': 'Ja'},
    {'type': 'Nee'},
]

uitvoering_choicelist = [
    {'type': 'Tweezijdig'},
    {'type': 'Eenzijdig'},
    {'type': 'Tweezijdig verschillend'},
]

standen_choicelist_clone = [
    {'type': 'Wijzig stand'},
    {'type': 'staand'},
    {'type': 'liggend'},
    {'type': 'vierkant'},
]

uitvoering_choicelist_clone = [
    {'type': 'Wijzig uitvoering bedrukking'},
    {'type': 'Eenzijdig'},
    {'type': 'Tweezijdig gelijk'},
    {'type': 'Tweezijdig verschillend'},
]

vernis_choicelist_clone = [
    {'type': 'Wijzig persvernis'},
    {'type': 'Nee'},
    {'type': 'Ja'},
]

productgroep_choices = (
    ('Drukvellen', 'Drukvellen'),
    ('Plano producten', 'Plano producten'),
    ('Folders', 'Folders'),
    ('Selfcovers', 'Selfcovers'),
    ('Brochures', 'Brochures'),
    ('Enveloppen', 'Enveloppen')
)
aanvraag_status_choices = (
    ('Aanvraag', 'Aanvraag'),
    ('Order', 'Order'),
    ('Clone', 'Clone'),
    ('Vervallen', 'Vervallen')

)

nabewerking_boeken_choices = (
    ('garen', 'Garenloos gebrocheerd'),
    ('pur', 'Garenloos gebrocheerd PUR'),
    ('perfo', 'Garenloos gebrocheerd perfobinding'),
    ('naaien', 'Genaaid gebrocheerd'),

)

formaat_choices = (
    ('type', 'kies formaattype'),
    ('standaard', 'standaardformaat'),
    ('vrij', 'vrij formaat'),
)

persvernis_choices = (
    ('Ja', 'Ja'),
    ('Nee', 'Nee')
)

omslag_choices = (
    ('met', "brochure met 4 pagina's omslag"),
    ('self', 'selfcover (geen omslag)'),
)

veredeling_zijden_omslag = (
    ('gn', 'geen veredeling'),
    ('ez', 'veredeling buitenzijde omslag)'),
)

veredeling_zijden_plano = (
    ('gn', 'geen veredeling'),
    ('ez', 'veredeling alleen op de voorzijde'),
    ('twg', 'tweezijdig gelijke veredeling'),
    ('twv', 'tweezijdig verschillende veredeling'),
)

maxdrukformaat_choices = (
    ('klein', 'tot 36x52cm'),
    ('midden', 'tot 52x74cm'),
    ('groot', 'tot 74 x 104cm'),
)

omslag_veredeling_choices = (
    ('Geen veredeling', 'Geen veredeling'),
    ('Mat lak', 'Mat lak'),
    ('Glans lak', 'Glans lak'),
    ('Dispersie lak', 'Dispersie lak'),
    ('UV lak', 'UV lak'),
    ('Mat lamineren', 'Mat lamineren'),
    ('Glans lamineren', 'Glans lamineren'),
    ('Krasvast mat lamineren', 'Krasvast mat lamineren'),
)

bedrukking_choices = (
    ('Zwart', 'Zwart'),
    ('Full Colour', 'Full color (YMCK)'),
    ('Alleen PMS kleuren', 'Alleen PMS kleuren'),
)

bedrukking_choices_zonderpms = (
    ('Zwart', 'Zwart'),
    ('Full Colour', 'Full color (YMCK)'),
)

uitvoering_choices = (
    ('Eenzijdig', 'Eenzijdig'),
    ('Tweezijdig gelijk', 'Tweezijdig gelijk'),
    ('Tweezijdig verschillend', 'Tweezijdig verschillend'),
)

verpakking_choicelist_clone = [
    {'type': 'Wijzig verpakking'},
    {'type': 'Afgestapeld op pallets'},
    {'type': 'Gebundeld op pallets'},
    {'type': 'Handzaam in dozen'},
    {'type': 'Per stuk gesealed'},
    {'type': 'Per stuk gesealed in dozen'},
]
veredeling_choicelist = [
    {'type': 'Geen veredeling'},
    {'type': 'Mat lak'},
    {'type': 'Glans lak'},
    {'type': 'Dispersie lak'},
    {'type': 'UV lak'},
    {'type': 'Mat lamineren'},
    {'type': 'Glans lamineren'},
]

veredeling_choicelist_clone = [
    {'type': 'Wijzig veredeling'},
    {'type': 'Geen veredeling'},
    {'type': 'Mat lak'},
    {'type': 'Glans lak'},
    {'type': 'Dispersie lak'},
    {'type': 'UV lak'},
    {'type': 'Mat lamineren'},
    {'type': 'Glans lamineren'},
]

veredeling_dictlist = [
    {'Geen veredeling': 'Geen veredeling'},
    {'Mat lak': 'Mat lak'},
    {'Glans lak': 'Glans lak'},
    {'Dispersie lak': 'Dispersie lak'},
    {'UV lak': 'UV lak'},
    {'Mat lamineren': 'Mat lamineren'},
    {'Glans lamineren': 'Glans lamineren'},
]

nabewerking_selfcover_choicelist = (
    {'type': 'Twee nietjes'},
    {'type': 'Twee oognieten'},
    {'type': 'Vier nietjes'},
    {'type': 'Vier oognieten'},
    {'type': 'Cahiersteek'},
    {'type': 'Singersteek'},
)

nabewerking_selfcover_choicelist_clone = (
    {'type': 'Wijzig nabewerking'},
    {'type': 'Twee nietjes'},
    {'type': 'Twee oognieten'},
    {'type': 'Vier nietjes'},
    {'type': 'Vier oognieten'},
    {'type': 'Cahiersteek'},
    {'type': 'Singersteek'},
)

nabewerking_brochures_choicelist = (
    {'type': 'Twee nietjes'},
    {'type': 'Twee oognieten'},
    {'type': 'Vier nietjes'},
    {'type': 'Vier oognieten'},
    {'type': 'Cahiersteek'},
    {'type': 'Singersteek'},
    {'type': 'Garenloos gebrocheerd'},
    {'type': 'Garenloos gebrocheerd PUR'},
    {'type': 'Garenloos gebrocheerd perfobinding'},
    {'type': 'Genaaid gebrocheerd'},
)

nabewerking_brochures_choicelist_clone = (
    {'type': 'Wijzig nabewerking'},
    {'type': 'Twee nietjes'},
    {'type': 'Twee oognieten'},
    {'type': 'Vier nietjes'},
    {'type': 'Vier oognieten'},
    {'type': 'Cahiersteek'},
    {'type': 'Singersteek'},
    {'type': 'Garenloos gebrocheerd'},
    {'type': 'Garenloos gebrocheerd PUR'},
    {'type': 'Garenloos gebrocheerd perfobinding'},
    {'type': 'Genaaid gebrocheerd'},
)
