# Generated by Django 3.2.9 on 2022-12-01 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0028_activitymodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='tweetmodel',
            name='is_retweet',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
