# Generated by Django 5.0.6 on 2024-09-03 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index', '0002_initial'),
        ('members', '0002_initial'),
        ('methods', '0001_initial'),
        ('printprojects', '0001_initial'),
        ('profileuseraccount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='brochurefinishingmethods',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='brochurefinishingmethods',
            name='productcategory',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
        migrations.AddField(
            model_name='enhancementoptions',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='foldingmethods',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='notes',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='members.clients'),
        ),
        migrations.AddField(
            model_name='notes',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='notes',
            name='printproject',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='printprojects.printprojects'),
        ),
        migrations.AddField(
            model_name='notes',
            name='producer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='notes',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='packagingoptions',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='standardsize',
            name='productcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
        migrations.AddField(
            model_name='transportoptions',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
    ]
