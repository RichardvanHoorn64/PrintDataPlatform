# Generated by Django 5.0.6 on 2024-05-09 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('calculations', '0001_initial'),
        ('index', '0001_initial'),
        ('offers', '0001_initial'),
        ('printprojects', '0001_initial'),
        ('profileuseraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='calculations',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='calculations',
            name='offer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offers.offers'),
        ),
        migrations.AddField(
            model_name='calculations',
            name='printproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='printprojects.printprojects'),
        ),
        migrations.AddField(
            model_name='calculations',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='calculations',
            name='productcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
    ]
