# Generated by Django 3.0.7 on 2020-06-27 10:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('AlbumsBackend', '0003_auto_20200627_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='albummodel',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
