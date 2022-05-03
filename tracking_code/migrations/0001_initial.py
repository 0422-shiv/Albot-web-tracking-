# Generated by Django 4.0.1 on 2022-02-02 17:58

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TrackingCode',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('company_name', models.CharField(blank=True, max_length=255, null=True)),
                ('web_page_name', models.CharField(blank=True, max_length=255, null=True)),
                ('script_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'tracking_code',
            },
        ),
        migrations.CreateModel(
            name='VisitorsLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('update_at', models.DateTimeField(auto_now=True, null=True)),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('browser', models.CharField(blank=True, max_length=255, null=True)),
                ('visitors', models.BigIntegerField(blank=True, null=True)),
                ('js_id', models.TextField(blank=True, editable=False, null=True)),
                ('time_on_page', models.BigIntegerField(blank=True, default=0, null=True)),
            ],
            options={
                'db_table': 'visitors_log',
            },
        ),
    ]
