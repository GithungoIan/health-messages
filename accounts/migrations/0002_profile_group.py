# Generated by Django 3.2.7 on 2021-09-09 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='group',
            field=models.CharField(blank=True, choices=[('hiv_aids', 'HIV / AIDS Group')], max_length=100, null=True),
        ),
    ]
