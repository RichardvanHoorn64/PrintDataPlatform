# Generated by Django 5.0.6 on 2024-09-03 10:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('index', '0002_initial'),
        ('members', '0002_initial'),
        ('printprojects', '0001_initial'),
        ('profileuseraccount', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='memberproducermatch',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='memberproducermatch',
            name='producer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='memberproducerstatus',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='memberproducermatch',
            name='memberproducerstatus',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='printprojects.memberproducerstatus'),
        ),
        migrations.AddField(
            model_name='printprojectmatch',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='printprojectmatch',
            name='memberproducermatch',
            field=models.ForeignKey(default=2, null=True, on_delete=django.db.models.deletion.CASCADE, to='printprojects.memberproducermatch'),
        ),
        migrations.AddField(
            model_name='printprojectmatch',
            name='producer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='printprojectmatch',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='client',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.clients'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='clientcontact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='members.clientcontacts'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='member',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profileuseraccount.members'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='producer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.producers'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='productcategory',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='index.productcategory'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='printprojectmatch',
            name='printproject',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='printprojects.printprojects'),
        ),
        migrations.AddField(
            model_name='printprojectstatus',
            name='language',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='profileuseraccount.languages'),
        ),
        migrations.AddField(
            model_name='printprojects',
            name='printprojectstatus',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='printprojects.printprojectstatus'),
        ),
    ]
