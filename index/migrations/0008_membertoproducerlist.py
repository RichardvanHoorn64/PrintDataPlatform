# Generated by Django 5.1.1 on 2024-11-28 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0007_alter_whitelistemail_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MemberToProducerList',
            fields=[
                ('convert_id', models.IntegerField(primary_key=True, serialize=False)),
                ('member_id', models.IntegerField()),
                ('to_convert', models.BooleanField(default=True)),
            ],
        ),
    ]