# Generated by Django 3.0.7 on 2020-06-27 10:19

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('AlbumsBackend', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='albummodel',
            name='songs',
        ),
        migrations.AlterField(
            model_name='albummodel',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='songmodel',
            name='album',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tracks', to='AlbumsBackend.AlbumModel'),
        ),
    ]
