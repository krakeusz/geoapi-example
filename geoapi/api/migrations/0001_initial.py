# Generated by Django 3.2.7 on 2021-09-06 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='IpGeolocationData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('continent_name', models.CharField(max_length=50)),
                ('country_name', models.CharField(max_length=100)),
                ('region_name', models.CharField(max_length=400)),
                ('city', models.CharField(max_length=400)),
                ('zip_code', models.CharField(max_length=20)),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=17)),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=18)),
            ],
        ),
    ]