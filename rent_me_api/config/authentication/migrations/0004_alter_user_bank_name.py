# Generated by Django 3.2.7 on 2021-09-23 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_auto_20210923_1104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank_name',
            field=models.CharField(default='My_Bank', max_length=50),
        ),
    ]
