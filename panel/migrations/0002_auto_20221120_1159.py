# Generated by Django 3.2.9 on 2022-11-20 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedauthuser',
            name='pending_verification',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name='extendedauthuser',
            name='role',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
