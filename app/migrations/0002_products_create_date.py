# Generated by Django 4.2.2 on 2023-08-24 14:44

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='create_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]