# Generated by Django 3.2 on 2021-04-22 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_alter_row_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='squares',
            field=models.CharField(default='0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000', max_length=100),
        ),
    ]