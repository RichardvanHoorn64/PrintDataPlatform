# Generated by Django 5.1.1 on 2024-10-11 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('printprojects', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='memberproducermatch',
            name='auto_quote',
            field=models.BooleanField(default=False),
        ),
    ]
