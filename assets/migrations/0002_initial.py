# Generated by Django 5.0.6 on 2024-05-09 21:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('assets', '0001_initial'),
        ('methods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bindingmachines',
            name='finishingmethod',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='methods.brochurefinishingmethods'),
        ),
    ]
