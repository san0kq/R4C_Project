# Generated by Django 4.2.5 on 2023-09-26 22:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('robots', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RobotModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=2, unique=True, verbose_name='model')),
            ],
        ),
        migrations.AlterField(
            model_name='robot',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='robot',
            name='model',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='robots',
                related_query_name='robot',
                to='robots.robotmodel',
            ),
        ),
    ]
