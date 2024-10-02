from django.db import models
from profileuseraccount.models import Languages, Producers


class CheckDomains(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=200, null=True, blank=True)
    excluded = models.BooleanField(default=False)
    update_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = 'domains'
        verbose_name_plural = 'domain'


class DropdownCountries(models.Model):
    country_id = models.AutoField(primary_key=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    country_code = models.CharField(max_length=10, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.country

    class Meta:
        verbose_name = 'countries'
        verbose_name_plural = 'country'


class DropdownChoices(models.Model):
    dropdown_id = models.AutoField(primary_key=True)
    dropdown = models.CharField(max_length=200, null=True, blank=True)
    value = models.PositiveIntegerField(default=0)
    text = models.CharField(max_length=200, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.dropdown

    class Meta:
        verbose_name = 'dropdowns'
        verbose_name_plural = 'dropdown'


class ProductCategory(models.Model):
    productcategory_id = models.AutoField(primary_key=True)
    productcategory = models.CharField(max_length=100, unique=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.productcategory

    class Meta:
        verbose_name = 'productcategories'
        verbose_name_plural = 'productcategory'


class Faqs(models.Model):
    faq_id = models.AutoField(primary_key=True)
    header = models.CharField(max_length=200, null=True, blank=True)
    sequence = models.PositiveIntegerField(default=1)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    question = models.CharField(max_length=1000, null=True, blank=True)
    answer = models.CharField(max_length=1000, null=True, blank=True)
    text = models.CharField(max_length=10000, null=True, blank=True)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'questions'
        verbose_name_plural = 'question'

    class Messages(models.Model):
        message_id = models.AutoField(primary_key=True)
        name = models.CharField(max_length=1000, null=True, blank=True)
        email = models.CharField(max_length=1000, null=True, blank=True)
        message = models.CharField(max_length=10000, null=True, blank=True)
        language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
        submit_date = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.message

        class Meta:
            verbose_name = 'messages'
            verbose_name_plural = 'message'


class Conditions(models.Model):
    condition_id = models.AutoField(primary_key=True)
    sequence = models.PositiveIntegerField(default=1)
    header = models.CharField(max_length=200, null=True, blank=True)
    condition = models.CharField(max_length=1000, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.header

    class Meta:
        verbose_name = 'headers'
        verbose_name_plural = 'header'


class Events(models.Model):
    event_id = models.AutoField(primary_key=True)
    sequence = models.PositiveIntegerField(default=1)
    event_name = models.CharField(max_length=200, null=True, blank=True)
    event_speaker = models.CharField(max_length=200, null=True, blank=True)
    event_description = models.CharField(max_length=2000, null=True, blank=True)
    event_date = models.DateTimeField(null=True, blank=True)
    event_time = models.CharField(max_length=200, null=True, blank=True)
    event_host = models.CharField(max_length=200, null=True, blank=True)
    event_location = models.CharField(max_length=500, null=True, blank=True)
    event_link = models.URLField(null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = 'events'
        verbose_name_plural = 'event'


class Texts(models.Model):
    text_id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=1000, null=True, blank=True)
    identifier = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'texts'
        verbose_name_plural = 'text'


class BrandPortalData(models.Model):
    producer = models.ForeignKey(Producers, on_delete=models.CASCADE)
    brandportal = models.CharField(max_length=200, blank=True, null=True)
    host = models.CharField(max_length=200, blank=True, null=True)
    brand_name = models.CharField(max_length=200, blank=True, null=True)
    brand_payoff = models.CharField(max_length=300, blank=True, null=True)

    contact_email = models.CharField(max_length=400, blank=True, null=True)
    contact_name = models.CharField(max_length=400, blank=True, null=True)
    loc_order_supply = models.CharField(max_length=400, blank=True, null=True)

    doc_loc_offer_1 = models.CharField(max_length=400, blank=True, null=True)
    doc_loc_offer_2 = models.CharField(max_length=400, blank=True, null=True)
    doc_loc_offer_3 = models.CharField(max_length=400, blank=True, null=True)
    doc_loc_offer_4 = models.CharField(max_length=400, blank=True, null=True)
    doc_loc_offer_5 = models.CharField(max_length=400, blank=True, null=True)
    doc_loc_offer_6 = models.CharField(max_length=400, blank=True, null=True)

    img_bg_loc_inlog = models.CharField(max_length=400, blank=True, null=True)

    img_loc_logo = models.CharField(max_length=400, blank=True, null=True)
    img_loc_logo_lg = models.CharField(max_length=400, blank=True, null=True)
    img_loc_logo_sm = models.CharField(max_length=400, blank=True, null=True)
    img_loc_sheets = models.CharField(max_length=400, blank=True, null=True)
    img_loc_plano = models.PositiveIntegerField(default=1)
    img_loc_folders = models.PositiveIntegerField(default=2)
    img_loc_selfcovers = models.PositiveIntegerField(default=3)
    img_loc_brochures = models.PositiveIntegerField(default=4)
    img_loc_books = models.PositiveIntegerField(default=5)

    brandcolor_bg = models.CharField(max_length=50, blank=True, null=True)
    brandcolor_font = models.CharField(max_length=50, blank=True, null=True)
    brandcolor_header = models.CharField(max_length=50, blank=True, null=True)

    brandportal_exclusive = models.BooleanField(default=True)
    brandportal_exclusive_open = models.BooleanField(default=True)

    brandportal_show_papercategoy = models.BooleanField(default=True)
    brandportal_show_papercolor = models.BooleanField(default=True)
    brandportal_show_pms_input = models.BooleanField(default=True)
    brandportal_show_orders = models.BooleanField(default=True)

    def __str__(self):
        return self.brand_name

    class Meta:
        verbose_name = 'Brandportal'
        verbose_name_plural = 'Brandportals'


class Blacklist(models.Model):
    blacklist_id = models.AutoField(primary_key=True)
    blacklist_text = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.blacklist_text

    class Meta:
        verbose_name = 'blacklist_texts'
        verbose_name_plural = 'blacklist_text'


class Whitelist(models.Model):
    whitelist_id = models.AutoField(primary_key=True)
    whitelist_text = models.CharField(max_length=1000, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    subject = models.CharField(max_length=1000, null=True, blank=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    def __str__(self):
        return self.whitelist_text

    class Meta:
        verbose_name = 'whitelist_texts'
        verbose_name_plural = 'whitelist_text'
