# Generated by Django 3.2.9 on 2022-11-30 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0023_auto_20221130_2006'),
    ]

    operations = [
        migrations.AddField(
            model_name='extendedauthuser',
            name='tweets',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]