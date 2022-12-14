# Generated by Django 3.2.9 on 2022-11-30 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('panel', '0025_tweetmodel_comment_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentLikeModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked', models.BooleanField(blank=True, default=False, null=True)),
                ('created_on', models.DateTimeField(default=django.utils.timezone.now)),
                ('parent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='panel.commentmodel')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'comment_like_tbl',
                'db_table': 'comment_like_tbl',
            },
        ),
    ]
