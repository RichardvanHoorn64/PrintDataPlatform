# Generated by Django 5.0.6 on 2024-09-03 10:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index', '0002_initial'),
        ('offers', '0001_initial'),
        ('printprojects', '0001_initial'),
        ('profileuseraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='offers',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='offers',
            name='printproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='printprojects.printprojects'),
        ),
        migrations.AddField(
            model_name='offers',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='offers',
            name='productcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
        migrations.AddField(
            model_name='offers',
            name='offerstatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='offers.offerstatus'),
        ),
    ]
