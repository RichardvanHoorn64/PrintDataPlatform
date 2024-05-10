# Generated by Django 5.0.6 on 2024-05-09 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='APIs',
            fields=[
                ('api_id', models.AutoField(primary_key=True, serialize=False)),
                ('api', models.CharField(default=0, max_length=200)),
                ('api_producer_id', models.PositiveIntegerField(blank=True, null=True)),
                ('api_client_id', models.PositiveIntegerField(blank=True, null=True)),
                ('producer', models.CharField(max_length=200)),
                ('producer_api_key', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'connections',
                'verbose_name_plural': 'connection',
            },
        ),
    ]
