# Generated by Django 3.2 on 2021-04-23 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_game_squares'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='position',
            field=models.IntegerField(default=1),
        ),
    ]
