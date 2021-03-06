# Generated by Django 3.2 on 2021-07-01 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_auto_20210630_2132'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseeker',
            name='resume',
            field=models.FileField(blank=True, null=True, upload_to='documents/'),
        ),
        migrations.AlterField(
            model_name='employer',
            name='profilepic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
