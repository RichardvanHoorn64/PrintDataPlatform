# Generated by Django 5.1.1 on 2024-10-02 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='conditions',
            options={'verbose_name': 'headers', 'verbose_name_plural': 'header'},
        ),
        migrations.AddField(
            model_name='conditions',
            name='header',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]