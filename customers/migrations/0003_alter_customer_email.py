# Generated by Django 4.2.5 on 2023-09-29 17:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('customers', '0002_alter_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]