# Generated by Django 3.1.4 on 2021-01-09 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Owner', '0006_auto_20210109_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee_reg_tb',
            name='password',
            field=models.CharField(default='No password', max_length=20),
        ),
        migrations.AddField(
            model_name='employee_reg_tb',
            name='username',
            field=models.CharField(default='No username', max_length=20),
        ),
    ]
