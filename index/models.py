from django.db import models
from profileuseraccount.models import Languages, Producers


class MemberToProducerList(models.Model):
    convert_id = models.IntegerField(primary_key=True)
    member_id = models.IntegerField()
    to_convert = models.BooleanField(default=True)


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


class BlacklistEmail(models.Model):
    blacklist_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    excluded = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'BlacklistsEmails'
        verbose_name_plural = 'BlacklistEmail'


class WhitelistEmail(models.Model):
    whitelist_id = models.AutoField(primary_key=True)
    email = models.CharField(max_length=1000, null=True, blank=True)
    excluded = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'WhitelistEmails'
        verbose_name_plural = 'WhitelistEmail'


class BlacklistDomains(models.Model):
    domain_id = models.AutoField(primary_key=True)
    domain = models.CharField(max_length=200, null=True, blank=True)
    excluded = models.BooleanField(default=True)

    def __str__(self):
        return self.domain

    class Meta:
        verbose_name = 'Blacklistdomains'
        verbose_name_plural = 'Blacklistdomain'
