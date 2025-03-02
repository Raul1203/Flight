# Generated by Django 5.1.6 on 2025-02-27 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Flight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('flight_number', models.CharField(max_length=10, unique=True)),
                ('airline', models.CharField(max_length=100)),
                ('origin', models.CharField(max_length=100)),
                ('destination', models.CharField(max_length=100)),
                ('departure_time', models.DateTimeField()),
                ('arrival_time', models.DateTimeField()),
                ('status', models.CharField(choices=[('scheduled', 'Scheduled'), ('active', 'Active'), ('landed', 'Landed'), ('cancelled', 'Cancelled'), ('delayed', 'Delayed')], default='scheduled', max_length=20)),
                ('aircraft', models.CharField(blank=True, max_length=50, null=True)),
                ('gate', models.CharField(blank=True, max_length=10, null=True)),
                ('terminal', models.CharField(blank=True, max_length=10, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
