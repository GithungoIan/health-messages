# Generated by Django 3.2.7 on 2021-09-09 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_broadcastmessage_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcastmessage',
            name='group',
            field=models.CharField(blank=True, choices=[('hiv_aids', 'HIV / AIDS Group'), ('cancer', 'Cancer Group')], max_length=100, null=True),
        ),
    ]
