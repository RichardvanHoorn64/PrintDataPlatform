# Generated by Django 5.0.6 on 2024-05-16 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('methods', '0003_brochurefinishingmethods_productcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='standardsize',
            name='standard',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
