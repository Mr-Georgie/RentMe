# Generated by Django 3.2.7 on 2021-09-27 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ReloadlyData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('receiver_phone', models.CharField(max_length=20)),
                ('sender_phone', models.CharField(max_length=20)),
                ('operator_id', models.CharField(max_length=6)),
                ('transaction_id', models.CharField(max_length=20)),
                ('operator_name', models.CharField(max_length=20)),
                ('amount', models.CharField(max_length=20)),
            ],
        ),
    ]
