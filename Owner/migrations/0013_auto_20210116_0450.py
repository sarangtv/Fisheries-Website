# Generated by Django 3.1.4 on 2021-01-16 04:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0012_fisher_fish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fisher_fish',
            name='price',
            field=models.FloatField(),
        ),
    ]
