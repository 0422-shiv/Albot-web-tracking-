# Generated by Django 4.0.1 on 2022-02-03 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('my_plan', '0002_monthlyplans_no_of_trial_days_monthlyplans_plan_type_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='subscription',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription_plan', to='my_plan.monthlyplans', verbose_name='subscription plan'),
        ),
    ]
