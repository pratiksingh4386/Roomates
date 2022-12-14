# Generated by Django 4.0.6 on 2022-08-07 17:56

from django.db import migrations, models
import hostel.models


class Migration(migrations.Migration):

    dependencies = [
        ('hostel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hostelite',
            fields=[
                ('name', models.CharField(max_length=100)),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='M', max_length=10)),
                ('sic', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('year', models.IntegerField(choices=[(2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021), (2022, 2022)], default=hostel.models.current_year, verbose_name='year')),
            ],
        ),
        migrations.DeleteModel(
            name='Hostelites',
        ),
    ]
