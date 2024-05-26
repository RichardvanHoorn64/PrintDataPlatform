# Generated by Django 5.0.6 on 2024-05-22 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0004_rename_brandportal_ordershow_brandportaldata_brandportal_show_orders_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='brandportaldata',
            name='img_loc_envelopes',
        ),
        migrations.AddField(
            model_name='brandportaldata',
            name='img_loc_books',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brand_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brand_payoff',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brandcolor_bg',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brandcolor_font',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brandcolor_header',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='brandportal',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='contact_email',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='contact_name',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_1',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_2',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_3',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_4',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_5',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='doc_loc_offer_6',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='host',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_bg_loc_inlog',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_folders',
            field=models.PositiveIntegerField(default=2),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_logo',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_logo_lg',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_logo_sm',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_plano',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_selfcovers',
            field=models.PositiveIntegerField(default=3),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='img_loc_sheets',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
        migrations.AlterField(
            model_name='brandportaldata',
            name='loc_order_supply',
            field=models.CharField(blank=True, max_length=400, null=True),
        ),
    ]
