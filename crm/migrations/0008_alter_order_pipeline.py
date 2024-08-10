# Generated by Django 5.0.8 on 2024-08-10 00:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_alter_product_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='pipeline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='crm.salespipeline'),
        ),
    ]
