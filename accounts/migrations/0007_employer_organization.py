# Generated by Django 3.2 on 2021-06-27 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210627_0706'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='organization',
            field=models.CharField(default='', max_length=200),
        ),
    ]