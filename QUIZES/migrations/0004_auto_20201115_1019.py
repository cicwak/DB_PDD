# Generated by Django 3.1.1 on 2020-11-15 07:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('QUIZES', '0003_auto_20201115_1016'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quizer',
            old_name='lenght',
            new_name='length',
        ),
    ]
