# Create your models here.
# account models
from django.contrib.auth.models import AbstractUser
from django.db import models


class Languages(models.Model):
    language_id = models.AutoField(primary_key=True)
    language_code = models.CharField(max_length=10, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)


class MemberPlans(models.Model):
    id = models.AutoField(primary_key=True)
    member_plan_id = models.PositiveIntegerField(null=True)
    producer = models.BooleanField(default=False)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    plan_name = models.CharField(max_length=100)
    plan_tariff = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    feature1 = models.CharField(max_length=100, blank=True, null=True)
    feature2 = models.CharField(max_length=100, blank=True, null=True)
    feature3 = models.CharField(max_length=100, blank=True, null=True)
    feature4 = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True, blank=True, null=True)

    def __str__(self):
        return self.plan_name

    class Meta:
        verbose_name = 'Member_plan'
        verbose_name_plural = 'Member_plans'


class Producers(models.Model):
    producer_id = models.AutoField(primary_key=True)
    member_plan = models.ForeignKey(MemberPlans, null=True, on_delete=models.SET_NULL)
    manager = models.CharField(max_length=50, blank=True, null=True)
    user_admin = models.PositiveIntegerField(blank=True, null=True)
    company = models.CharField(max_length=100, unique=True)
    tel_general = models.CharField(max_length=15, blank=True, null=True)
    e_mail_general = models.EmailField(blank=True, null=True)
    street_number = models.CharField(max_length=30, blank=True, null=True)
    postal_code = models.CharField(max_length=7, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=100, default="NL")
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    demo_company = models.BooleanField(default=False)
    company_url = models.URLField(null=True, blank=True, max_length=200)


    # modules
    exclusive_module = models.BooleanField(default=False)
    calculation_module = models.BooleanField(default=False)
    brandportal_module = models.BooleanField(default=False)
    powerplatform_module = models.BooleanField(default=False)
    api_module = models.BooleanField(default=False)

    # api settings
    api_active = models.BooleanField(default=False)
    api_function = models.CharField(max_length=200, blank=True, null=True)
    api_url = models.CharField(max_length=300, blank=True, null=True)
    response_score = models.PositiveIntegerField(default=1, null=True)
    automated_score = models.PositiveIntegerField(default=1, null=True)
    win_score = models.PositiveIntegerField(default=1, null=True)
    doc_templates = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    demo = models.BooleanField(default=False)
    uploaded_by = models.CharField(max_length=500, blank=True)

    def __str__(self):
        return self.company

    class Meta:
        verbose_name = 'producer'
        verbose_name_plural = 'producers'


class Members(models.Model):
    member_id = models.AutoField(primary_key=True)
    member_plan = models.ForeignKey(MemberPlans, null=True, on_delete=models.SET_NULL)
    producerplan = models.BooleanField(default=False)
    # This member is exclusive for  producer or is producer
    exclusive_producer = models.ForeignKey(Producers, null=True,
                                           on_delete=models.SET_NULL)
    manager = models.CharField(max_length=50, unique=False, default='')
    user_admin = models.PositiveIntegerField(blank=True, null=True)
    company = models.CharField(max_length=100, unique=True)
    tel_general = models.CharField(max_length=15, blank=True)
    e_mail_general = models.EmailField(blank=True)
    street_number = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    country_code = models.CharField(max_length=100, default="NL")
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)
    demo_company = models.BooleanField(default=False)

    # social media
    linkedin_url = models.URLField(null=True, blank=True, max_length=200)
    company_url = models.URLField(null=True, blank=True, max_length=200)

    doc_templates = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)


    def __str__(self):
        return self.company

    class Meta:
        verbose_name = 'Member'
        verbose_name_plural = 'Members'


class UserProfile(AbstractUser):
    pass
    producer = models.ForeignKey(Producers, blank=True, null=True, on_delete=models.SET_NULL)
    member = models.ForeignKey(Members, blank=True, null=True, on_delete=models.SET_NULL)
    member_plan = models.ForeignKey(MemberPlans, null=True, on_delete=models.SET_NULL)
    jobtitle = models.CharField(max_length=25, blank=True)
    company = models.CharField(max_length=100)
    tel_general = models.CharField(max_length=15, blank=True)
    mobile_number = models.CharField(max_length=15, blank=True)
    e_mail_general = models.EmailField(blank=True)
    street_number = models.CharField(max_length=30, blank=True)
    postal_code = models.CharField(max_length=7, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country_code = models.CharField(max_length=100, default="NL")
    first_user = models.BooleanField(default=True)
    language = models.ForeignKey(Languages, null=True, blank=True, default=1, on_delete=models.SET_NULL)

    # social media
    linkedin_url = models.URLField(null=True, blank=True, max_length=200)
    company_url = models.URLField(null=True, blank=True, max_length=200)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True or "")
    active = models.BooleanField(default=True)


    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'


USERNAME_FIELD = 'username'
REQUIRED_FIELDS = ['username', "email", 'first_name', 'last_name', 'company', ]
