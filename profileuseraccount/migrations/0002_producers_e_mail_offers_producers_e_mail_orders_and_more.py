# Generated by Django 5.0.6 on 2024-09-10 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profileuseraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producers',
            name='e_mail_offers',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='producers',
            name='e_mail_orders',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AddField(
            model_name='producers',
            name='e_mail_rfq',
            field=models.EmailField(blank=True, max_length=254),
        ),
    ]
