# Generated by Django 2.2.4 on 2019-08-14 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReviewsApp', '0002_review_date_added'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='session_key',
            field=models.CharField(blank=True, default=None, max_length=128, null=True),
        ),
    ]
