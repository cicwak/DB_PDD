# Generated by Django 3.1.1 on 2020-10-26 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PROFILES',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_profiles', models.IntegerField()),
                ('passed', models.TextField()),
                ('Points', models.TextField()),
                ('Scanned', models.TextField()),
            ],
        ),
    ]