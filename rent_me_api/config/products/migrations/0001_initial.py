# Generated by Django 3.2.7 on 2021-09-17 15:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('category', models.CharField(choices=[('GADGETS', 'GADGETS'), ('ELECTRONICS', 'ELECTRONICS'), ('AUTOMOBILE', 'AUTOMOBILE'), ('AGRICULTURAL', 'AGRICULTURAL')], max_length=255)),
                ('price', models.IntegerField()),
                ('description', models.TextField()),
                ('date_created', models.DateField(auto_now_add=True)),
                ('on_loan', models.BooleanField(default=False)),
                ('image', models.ImageField(default='products/default.jpg', upload_to=products.models.upload_to, verbose_name='Image')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
