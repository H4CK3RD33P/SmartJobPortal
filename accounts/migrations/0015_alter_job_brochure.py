# Generated by Django 3.2 on 2021-07-07 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_job_brochure'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='brochure',
            field=models.FilePathField(blank=True, null=True, path='/home/devildeep/Desktop/Projects/onlinejobportal/media/documents'),
        ),
    ]
