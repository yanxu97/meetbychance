# Generated by Django 2.1.7 on 2019-03-22 20:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190322_1846'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='travel_plan',
            unique_together={('plan_id', 'country', 'state', 'city', 'start_time', 'end_time')},
        ),
    ]