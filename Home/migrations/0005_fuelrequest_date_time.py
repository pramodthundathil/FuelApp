# Generated by Django 3.1.1 on 2024-04-13 03:09

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0004_fuelrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='fuelrequest',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]