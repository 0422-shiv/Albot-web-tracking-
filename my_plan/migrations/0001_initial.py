# Generated by Django 4.0.1 on 2022-02-02 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPlans',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan', models.CharField(max_length=20)),
                ('per_month_charge', models.CharField(max_length=20)),
                ('linkedin_warm_up', models.BooleanField(default=False)),
                ('email_warm_up', models.BooleanField(default=False)),
                ('daily_email_limit', models.IntegerField()),
                ('weekly_connection_limit', models.IntegerField()),
                ('email_enrichment', models.BooleanField(default=False)),
                ('linkedin_messages_free', models.IntegerField()),
                ('linkedin_messages_paid', models.IntegerField()),
                ('linkedIn_inmail_paid', models.IntegerField()),
                ('one_two_one_marketing', models.BooleanField(default=False)),
                ('view_prospects_profile', models.BooleanField(default=False)),
                ('like_prospect_recent_post', models.BooleanField(default=False)),
                ('endorse_linkedin_profile', models.BooleanField(default=False)),
                ('crm_Management', models.BooleanField(default=False)),
                ('crm_export', models.BooleanField(default=False)),
                ('social_content', models.BooleanField(default=False)),
                ('profile_views', models.BooleanField(default=False)),
                ('ssi_seo', models.BooleanField(default=False)),
                ('score_inbox_management', models.BooleanField(default=False)),
            ],
        ),
    ]