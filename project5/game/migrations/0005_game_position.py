# Generated by Django 3.2 on 2021-04-22 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_remove_row_visit'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='position',
            field=models.CharField(default='A0', max_length=2),
        ),
    ]
