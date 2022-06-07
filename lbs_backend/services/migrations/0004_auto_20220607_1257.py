# Generated by Django 3.2.12 on 2022-06-07 09:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_requestresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestresponse',
            name='ProviderID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='provider', to='services.serviceprovider'),
        ),
        migrations.AlterField(
            model_name='requestresponse',
            name='RequestID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='request', to='services.servicerequest'),
        ),
    ]
