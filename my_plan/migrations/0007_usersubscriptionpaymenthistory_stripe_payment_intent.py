# Generated by Django 4.0.1 on 2022-02-21 09:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_plan', '0006_stripekeys'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscriptionpaymenthistory',
            name='stripe_payment_intent',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]