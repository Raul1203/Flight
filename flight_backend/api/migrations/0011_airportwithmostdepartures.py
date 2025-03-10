# Generated by Django 5.1.6 on 2025-03-05 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_alter_airplanelocation_latitude_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AirportWithMostDepartures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(unique=True)),
                ('airport', models.CharField(max_length=255)),
                ('departure_count', models.IntegerField()),
                ('airline_departure_counts', models.JSONField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
