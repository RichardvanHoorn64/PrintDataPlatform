# Generated by Django 5.0.6 on 2024-09-03 08:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0011_blacklist_whitelist'),
        ('profileuseraccount', '0017_members_mobile_number_producers_mobile_number_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('event_id', models.AutoField(primary_key=True, serialize=False)),
                ('sequence', models.PositiveIntegerField(default=1)),
                ('event_name', models.CharField(blank=True, max_length=200, null=True)),
                ('event_description', models.CharField(blank=True, max_length=2000, null=True)),
                ('event_date', models.DateTimeField(blank=True, null=True)),
                ('event_link', models.URLField(blank=True, null=True)),
                ('language', models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages')),
            ],
            options={
                'verbose_name': 'events',
                'verbose_name_plural': 'event',
            },
        ),
    ]
