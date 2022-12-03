# Generated by Django 3.2.9 on 2022-11-28 05:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0017_remove_likemodel_tweet_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True, null=True)),
                ('retweeted_id', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.tweetmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'comment_tbl',
                'db_table': 'comment_tbl',
            },
        ),
    ]