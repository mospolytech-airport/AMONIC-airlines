# Generated by Django 4.2.5 on 2023-10-25 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure', models.CharField(max_length=200)),
                ('arrival', models.CharField(max_length=200)),
                ('age', models.IntegerField()),
                ('gender', models.CharField(max_length=200)),
                ('cabintype', models.CharField(max_length=200)),
                ('q1', models.IntegerField()),
                ('q2', models.IntegerField()),
                ('q3', models.IntegerField()),
                ('q4', models.IntegerField()),
            ],
        ),
    ]
