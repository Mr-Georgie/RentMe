# Generated by Django 3.2.7 on 2021-10-04 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_auto_20210924_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank_account_number',
            field=models.CharField(blank=True, default='0059227130', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bank_name',
            field=models.CharField(blank=True, default='Access', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(blank=True, default='Nigeria', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(blank=True, default='08144149628', max_length=50, null=True),
        ),
    ]
