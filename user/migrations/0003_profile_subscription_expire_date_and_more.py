# Generated by Django 4.0.1 on 2022-02-03 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_profile_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription_expire_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_start_date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='subscription_type',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
