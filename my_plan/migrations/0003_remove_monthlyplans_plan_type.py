# Generated by Django 4.0.1 on 2022-02-03 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_plan', '0002_monthlyplans_no_of_trial_days_monthlyplans_plan_type_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='monthlyplans',
            name='plan_type',
        ),
    ]
