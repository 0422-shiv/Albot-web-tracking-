# Generated by Django 4.0.1 on 2022-04-22 13:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('my_plan', '0011_plancancelrequest'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='contactus',
            options={'verbose_name': 'Contact Us', 'verbose_name_plural': 'Contact Us'},
        ),
        migrations.AlterModelOptions(
            name='monthlyplans',
            options={'verbose_name': 'Monthly Plan', 'verbose_name_plural': 'Monthly Plans'},
        ),
        migrations.AlterModelOptions(
            name='stripekeys',
            options={'verbose_name': 'Stripe Key', 'verbose_name_plural': 'Stripe Keys'},
        ),
        migrations.AlterModelOptions(
            name='usersubscriptionpaymenthistory',
            options={'verbose_name': 'User subscription payment history', 'verbose_name_plural': 'User subscription payment history'},
        ),
    ]
