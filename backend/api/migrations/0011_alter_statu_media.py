# Generated by Django 4.2.3 on 2024-01-07 22:51

import api.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_statu_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statu',
            name='media',
            field=models.FileField(blank=True, upload_to=api.models.status_directory_path),
        ),
    ]
