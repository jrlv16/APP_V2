# Generated by Django 4.0.4 on 2022-05-26 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alim', '0005_alter_order_options_alter_order_created_by_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_order',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date de commande'),
        ),
    ]
