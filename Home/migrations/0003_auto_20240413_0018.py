# Generated by Django 3.1.1 on 2024-04-12 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0002_fuelstocks'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fuelstocks',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]