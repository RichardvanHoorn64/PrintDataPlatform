# Generated by Django 5.0.6 on 2024-05-09 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PaperBrand',
            fields=[
                ('paperbrand_id', models.AutoField(primary_key=True, serialize=False)),
                ('papercategory', models.CharField(blank=True, max_length=250)),
                ('paperbrand', models.CharField(blank=True, max_length=250)),
                ('upload_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'paperbrand',
                'verbose_name_plural': 'paperbrands',
            },
        ),
        migrations.CreateModel(
            name='PaperBrandReference',
            fields=[
                ('paperbrandreference_id', models.AutoField(primary_key=True, serialize=False)),
                ('papercategory', models.CharField(blank=True, max_length=250)),
                ('paperbrand', models.CharField(blank=True, max_length=250)),
                ('folders', models.BooleanField(default=True)),
                ('brochures_interior', models.BooleanField(default=True)),
                ('brochures_cover', models.BooleanField(default=True)),
                ('description', models.CharField(blank=True, max_length=250, null=True)),
                ('link', models.URLField(blank=True, null=True)),
                ('FSC', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'paperbrand',
                'verbose_name_plural': 'paperbrands',
            },
        ),
        migrations.CreateModel(
            name='PaperCatalog',
            fields=[
                ('paperspec_id', models.AutoField(primary_key=True, serialize=False)),
                ('supplier', models.CharField(max_length=250)),
                ('supplier_number', models.CharField(max_length=250)),
                ('papercategory', models.CharField(max_length=250)),
                ('paperbrand', models.CharField(blank=True, max_length=250)),
                ('papercolor', models.CharField(blank=True, max_length=25, null=True)),
                ('paperweight_m2', models.PositiveIntegerField(blank=True, null=True)),
                ('paper_height_mm', models.PositiveIntegerField(blank=True, null=True)),
                ('paper_width_mm', models.PositiveIntegerField(blank=True, null=True)),
                ('paper_surface', models.PositiveIntegerField(blank=True, null=True)),
                ('fiber_direction', models.CharField(blank=True, max_length=250)),
                ('paper_thickening', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('sheets_per_pack', models.PositiveIntegerField(blank=True, null=True)),
                ('price_1000sheets', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('upload_date', models.DateField(null=True)),
                ('uploaded_by', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name': 'paper',
                'verbose_name_plural': 'papers',
            },
        ),
        migrations.CreateModel(
            name='PaperCategoryReference',
            fields=[
                ('papercategory_id', models.AutoField(primary_key=True, serialize=False)),
                ('papercategory', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name': 'papercategory',
                'verbose_name_plural': 'papercategories',
            },
        ),
        migrations.CreateModel(
            name='PaperWeights',
            fields=[
                ('paperweight_id', models.AutoField(primary_key=True, serialize=False)),
                ('papercategory', models.CharField(blank=True, max_length=250)),
                ('paperbrand', models.CharField(blank=True, max_length=250)),
                ('paperweight_m2', models.PositiveIntegerField(blank=True, null=True)),
                ('upload_date', models.DateField(null=True)),
            ],
            options={
                'verbose_name': 'paperweight',
                'verbose_name_plural': 'paperweights',
            },
        ),
        migrations.CreateModel(
            name='ProducerPaperCategory',
            fields=[
                ('producerpapercategory_id', models.AutoField(primary_key=True, serialize=False)),
                ('producerpapercategory', models.CharField(blank=True, max_length=250)),
            ],
            options={
                'verbose_name': 'producerpapercategory',
                'verbose_name_plural': 'producerpapercategories',
            },
        ),
    ]
