# Generated by Django 3.2.12 on 2022-06-07 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_servicerequest_requesttext'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ResponseText', models.TextField(blank=True, null=True)),
                ('Timestamp', models.DateTimeField(auto_now_add=True)),
                ('ProviderID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.serviceprovider')),
                ('RequestID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.servicerequest')),
            ],
            options={
                'verbose_name': 'Service Request Responses',
                'verbose_name_plural': 'Service Request Responses',
            },
        ),
    ]
