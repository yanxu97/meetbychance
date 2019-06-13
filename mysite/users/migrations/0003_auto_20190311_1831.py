# Generated by Django 2.1.7 on 2019-03-11 18:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_travel_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel_plan',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan', to=settings.AUTH_USER_MODEL),
        ),
    ]
