# Generated by Django 4.2.2 on 2023-08-25 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0032_cartitem_var'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(to='app.products'),
        ),
    ]