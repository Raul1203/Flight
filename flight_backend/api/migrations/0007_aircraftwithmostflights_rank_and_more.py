# Generated by Django 5.1.6 on 2025-03-04 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_remove_daywithmostflights_latitude_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='aircraftwithmostflights',
            name='rank',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='mostvisiteddestination',
            name='latest_landing',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mostvisiteddestination',
            name='rank',
            field=models.IntegerField(default=0),
        ),
    ]
