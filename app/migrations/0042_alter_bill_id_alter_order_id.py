# Generated by Django 4.2.2 on 2023-08-26 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0040_alter_bill_id_alter_order_id_squashed_0041_alter_bill_id_alter_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='order',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]