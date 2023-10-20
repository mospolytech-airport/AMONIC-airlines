# Generated by Django 4.2.5 on 2023-10-20 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Aircraft',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=50)),
                ('MakeModel', models.CharField(blank=True, max_length=10, null=True)),
                ('TotalSeats', models.IntegerField()),
                ('EconomySeats', models.IntegerField()),
                ('BusinessSeats', models.IntegerField()),
            ],
        ),
    ]