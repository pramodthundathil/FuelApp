# Generated by Django 3.1.1 on 2024-04-13 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0005_fuelrequest_date_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='FuelPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('petrol', models.FloatField()),
                ('diesel', models.FloatField()),
                ('lpg', models.FloatField()),
            ],
        ),
    ]
