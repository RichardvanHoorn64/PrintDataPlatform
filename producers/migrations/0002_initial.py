# Generated by Django 5.0.6 on 2024-05-09 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index', '0002_initial'),
        ('methods', '0002_initial'),
        ('producers', '0001_initial'),
        ('profileuseraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='enhancementtariffs',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='packagingtariffs',
            name='packagingoption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='methods.packagingoptions'),
        ),
        migrations.AddField(
            model_name='packagingtariffs',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='producercontacts',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='producercontacts',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='producerproductofferings',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='producerproductofferings',
            name='productcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
        migrations.AddField(
            model_name='transporttariffs',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='transporttariffs',
            name='transportoption',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='methods.transportoptions'),
        ),
    ]
