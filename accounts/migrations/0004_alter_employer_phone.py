# Generated by Django 3.2 on 2021-06-24 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_jobseeker_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employer',
            name='phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]